from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import ManualUploadForm
from django.db import connection
import sqlite3 

from .models import *
import datetime
import requests, sys
from bed_maker.externalAPIs import *
import markdown2
import os
from celery import shared_task


# Create your views here.
def home(request):
    with open('bed_maker/user_guides/user_guide.md') as f:
        markdown = f.read()
    return render(request, 'bed_maker/home.html', {
        "content": markdown2.markdown(markdown) 
    })

def view(request):
    """
    View a list of transcripts
    """
    context =  {}
    context['transcripts'] = Transcript.objects.all()

    return render(request, 'bed_maker/view.html', context)

# def SelectBedfile(request):
#     """
#     Provide List of BedfileRequests
#     """
#     # setup view
#     selected_form = BedfileSelectForm()
    
#     context = {'selected_form': selected_form,}
    
#     # if form is submitted
#     if request.method == 'POST':

#         selected_form = BedfileSelectForm(request.POST)
#         if selected_form.is_valid:
#             print(selected_form)
#             cleaned_data = selected_form.cleaned_data
#             selected_bedfile_request = cleaned_data['select_bedfile_request']          
#     # render the page
#     return render(request, 'bed_maker/edit.html', context)

def manual_import(request):
    """
    Takes the input from the manual input form and imports it into the database
    """
    # setup view
    import_form = ManualUploadForm()

    context = {'import_form': import_form, 'message' : None}
    print(context)    
    # if form is submitted
    if request.method == 'POST':

        import_form = ManualUploadForm(request.POST)
        if import_form.is_valid:
            print(import_form)
            cleaned_data = import_form.cleaned_data

            # Get list of all MANE Selected transcripts
            MANE_list_df = get_MANE_list()

           # get bedfile request data - BedfileRequest is created when the users fills in
           # the Import details in the webapp creating a BedfileRequest object which is defined in models.py
            bedfile_request, created = BedfileRequest.objects.get_or_create(
                pan_number = cleaned_data['pan_number'],
                date_requested = cleaned_data['date_requested'],
                requested_by = cleaned_data['requested_by'],
                request_status = 'draft',
                # request_transcript_padding = cleaned_data['request_transcript_padding'],
                request_introns = cleaned_data['request_introns'],
                request_exon_padding = cleaned_data['request_exon_padding'],
                request_five_prime_UTR = cleaned_data['request_five_prime_UTR'],
                request_three_prime_UTR = cleaned_data['request_three_prime_UTR'],
                request_five_prime_UTR_padding = cleaned_data['request_five_prime_UTR_padding'],
                request_three_prime_UTR_padding = cleaned_data['request_three_prime_UTR_padding'],
                panel_category = cleaned_data['panel_category'],
                panel_subcategory = cleaned_data['panel_subcategory'],
                panel_name = cleaned_data['panel_name'],
            )
            # Use the TARK API to get most recent version of the MANE transcript list
            # Get Gene list - Gene objects is defined in models.py - it populates the data into the 
            # genes table for every BedfileRequest made.
            # List comprehension to split lines input by user into a list and trim any white space
            gene_list = [y for y in (x.strip() for x in cleaned_data['gene_list'].splitlines()) if y]
            for gene_ID in gene_list:
                # Get data from ensembl
                ensembl_gene_data = lookup_ensembl_gene(gene_ID)
                # Populate database with transcript details for each gene using Ensembl API
                gene = Gene.objects.create(
                ensembl_id = gene_ID,
                bedfile_request_id = bedfile_request,
                display_name = ensembl_gene_data["display_name"],
                # TODO check if these should be added to model
                #y = ensembl_gene_data["biotype"],
                #z = ensembl_gene_data["seq_region_name"],
                )
                # Get Transcript level data
                for tx in ensembl_gene_data["Transcript"]:
                    try:
                        _coverage = ClinvarCoverage_grch37.objects.filter(transcript_ensembl_id=tx['id']).get().clinvar_coverage_fraction,
                    except:
                        _coverage = ''
                    # count gene variants and update covered clinvar fraction
                    transcript = Transcript.objects.create(
                    ensembl_id = tx['id'],
                    ensembl_transcript_version = tx['version'],
                    bedfile_request_id = bedfile_request,
                    gene_id = gene,
                    display_name = tx["display_name"],
                    chromosome = tx["seq_region_name"],
                    start = tx["start"],
                    end = tx["end"],
                    biotype = tx["biotype"],
                    coverage = _coverage,
                    # TODO Simplify dataframe to faster data structure
                    MANE_transcript = 'True' if tx["id"] in MANE_list_df.ens_stable_id.values else 'False',
                    RefSeq_transcript_id = MANE_list_df.loc[MANE_list_df['ens_stable_id'] == tx["id"]]['refseq_stable_id'].item() if tx["id"] in MANE_list_df.ens_stable_id.values else '',
                    RefSeq_transcript_version = MANE_list_df.loc[MANE_list_df['ens_stable_id'] == tx["id"]]['refseq_stable_id_version'].item() if tx["id"] in MANE_list_df.ens_stable_id.values else '',
                    # All other setting initialised as per bedfile global settings 
                    # transcript_padding = cleaned_data['request_transcript_padding'],
                    include_introns = cleaned_data['request_introns'],
                    include_exon_padding = cleaned_data['request_exon_padding'],
                    include_five_prime_UTR = cleaned_data['request_five_prime_UTR'],
                    include_three_prime_UTR = cleaned_data['request_three_prime_UTR'],
                    five_prime_UTR_padding = cleaned_data['request_five_prime_UTR_padding'],
                    three_prime_UTR_padding = cleaned_data['request_three_prime_UTR_padding'],
                    #clinvar_details = transcript_dict['clinvar_details'],
                    # TODO Update with M Yau's rules
                    recommended_transcript = 'True' if tx["id"] in MANE_list_df.ens_stable_id.values else 'False',
                    # TODO Update with M Yau's rules
                    selected_transcript = 'True' if tx["id"] in MANE_list_df.ens_stable_id.values else 'False',
                    )
                    for utr in tx["UTR"]:
                        utr = UTR.objects.create(
                        transcript_id = transcript,
                        bedfile_request_id = bedfile_request,
                        gene_id = gene,
                        ensembl_id = utr['id'],
                        utr_type = utr['type'],
                        start = utr["start"],
                        end = utr["end"],
                        )
                    for exon in tx["Exon"]:
                        exon = Exon.objects.create(
                        transcript_id = transcript,
                        ensembl_id = exon["id"],
                        ensembl_exon_version = exon["version"],
                        bedfile_request_id = bedfile_request,
                        gene_id = gene,
                        chromosome = exon['seq_region_name'],
                        start = tx["start"],
                        end = tx["end"],
                        )
            if cleaned_data["region_list"]:
                genomic_regions = [y for y in (x.strip() for x in cleaned_data['region_list'].splitlines()) if y]
                for genomic_region in genomic_regions:
                    region_id, region_chr, region_start, region_end = genomic_region.split(",")
                    genomic_range = GenomicRange.objects.create(
                    bedfile_request_id = bedfile_request,
                    genomic_region_id = region_id,
                    chromosome = region_chr,
                    start = region_start,
                    end = region_end,
                    )

            # add success message to page
            my_request_id = cleaned_data['pan_number']
            context['message'] = [f'User submitted Bed File Request "{my_request_id}" was processed successfully']
            print(context)
    # render the page
    return render(request, 'bed_maker/manual_import.html', context)
""