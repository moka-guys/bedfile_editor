from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import ManualUploadForm
from .models import *
import datetime
import requests, sys
from bed_maker.Clinvar.clinvar_coverage import annotate_transcripts,  lookup_ensembl_gene


# Create your views here.
def home(request):
    return render(request, 'bed_maker/home.html', {})

def view(request):
    """
    View a list of transcripts
    """
    transcript_list = Transcript.objects.all()

    return render(request, 'bed_maker/view.html', {'transcripts': transcript_list})

def manual_import(request):
    """
    Takes the input from the manual input form and imports it into the database
    """
    # setup view
    import_form = ManualUploadForm()

    context = {'import_form': import_form,}
    
    # if form is submitted
    if request.method == 'POST':

        import_form = ManualUploadForm(request.POST)
        if import_form.is_valid:
            print(import_form)
            cleaned_data = import_form.cleaned_data

           # get bedfile request data - BedfileRequest is created when the users fills in
           # the Import details in the webapp creating a BedfileRequest object which is defined in models.py
            bedfile_request, created = BedfileRequest.objects.get_or_create(
                pan_number = cleaned_data['pan_number'],
                date_requested = cleaned_data['date_requested'],
                requested_by = cleaned_data['requested_by'],
                request_status = 'draft',
            )

            # Use the TARK API to get most recent version of the MANE transcript list
            # Get Gene list - Gene objects is defined in models.py - it populates the data into the 
            # genes table for every BedfileRequest made.
            # List comprehension to split lines input by user into a list and trim any white space
            gene_list = [y for y in (x.strip() for x in cleaned_data['gene_list'].splitlines()) if y]
            for gene_ID in gene_list:
                gene = Gene.objects.create(
                ensembl_gene_id = gene_ID,
                bedfile_request_id = bedfile_request,
                )
                # Populate database with transcript details for each gene using Ensembl API
                gene_object = lookup_ensembl_gene(gene_ID)

                transcripts_annotated = annotate_transcripts(gene_object)
                
                for transcript_dict in transcripts_annotated:
                    # check if the Transcript ID is present in a list of all MANE transcripts, if it does it allocates True to the field MANE_transcript 
                    # and adds the appropriate RefSeq ID to the field
                  
                    transcript = Transcript.objects.create(
                    ensembl_transcript_id = transcript_dict["id"],
                    bedfile_request_id = bedfile_request,
                    gene_id = gene,
                    display_name = transcript_dict["display_name"],
                    start = transcript_dict["start"],
                    end = transcript_dict["end"],
                    MANE_transcript = transcript_dict['MANE_transcript'],
                    RefSeq_transcript_id = transcript_dict['RefSeq_transcript_id'],
                    coverage = round(transcript_dict['coverage'], 8),
                    clinvar_coverage = transcript_dict['clinvar_coverage'],
                    clinvar_variants = transcript_dict['clinvar_variants'] if transcript_dict['clinvar_variants'] else None,
                    clinvar_details = transcript_dict['clinvar_details']
                    )
            # add success message to page
            context['message'] = ['Gene list was uploaded successfully']

    # render the page
    return render(request, 'bed_maker/manual_import.html', context)