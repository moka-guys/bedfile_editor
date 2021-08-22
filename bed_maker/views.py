from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import ManualUploadForm
from .models import *
import datetime
import requests, sys
import pandas as pd

# Create your views here.
def home(request):
    return render(request, 'bed_maker/home.html', {})

def view(request):
    """
    View a list of transcripts
    """
    transcript_list = Transcript.objects.all()

    return render(request, 'bed_maker/view.html', {'transcripts': transcript_list})

def get_MANE_list():
    server = "http://dev-tark.ensembl.org"

    ext = f"/api/transcript/manelist/"
    
    r = requests.get(server+ext, headers={ "Content-Type" : "text/html"})
    
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    
    decoded = r.json()
    # ens_stable_id, ens_stable_id_version, refseq_stable_id, refseq_stable_id_version, mane_type, ens_gene_name
    MANE_list_df = pd.DataFrame(decoded) 
    
    return(MANE_list_df)  

def lookup_ensembl_gene(ensembl_gene_id):
    server = "https://rest.ensembl.org"

    ext = f"/lookup/id/{ensembl_gene_id}?expand=1&utr=1"
    
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    
    decoded = r.json()
    return(decoded)

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

           # get bedfile request data
            bedfile_request, created = BedfileRequest.objects.get_or_create(
                pan_number = cleaned_data['pan_number'],
                date_requested = cleaned_data['date_requested'],
                requested_by = cleaned_data['requested_by'],
                request_status = 'draft',
            )

            # Use the TARK API to get most recent version of the MANE transcript list

            MANE_list_df = get_MANE_list()

            # Get Gene list
            gene_list = [y for y in (x.strip() for x in cleaned_data['gene_list'].splitlines()) if y]
            for gene_ID in gene_list:
                gene = Gene.objects.create(
                ensembl_gene_id = gene_ID,
                bedfile_request_id = bedfile_request,
                )
                # Populate database with transcript details for each gene using Ensembl API
                gene_object = lookup_ensembl_gene(gene_ID)
                for transcript_dict in gene_object["Transcript"]:
                    if transcript_dict["id"] in MANE_list_df.ens_stable_id.values:
                        MANE_transcript = 'True'
                        RefSeq_transcript_id = MANE_list_df.loc[MANE_list_df['ens_stable_id'] == transcript_dict["id"]]['refseq_stable_id'].item()
                    else:
                        MANE_transcript = 'False'
                        RefSeq_transcript_id = ''
                    transcript = Transcript.objects.create(
                    ensembl_transcript_id = transcript_dict["id"],
                    bedfile_request_id = bedfile_request,
                    gene_id = gene,
                    display_name = transcript_dict["display_name"],
                    start = transcript_dict["start"],
                    end = transcript_dict["end"],
                    MANE_transcript = MANE_transcript,
                    RefSeq_transcript_id = RefSeq_transcript_id
                    )
            # add success message to page
            context['message'] = ['Gene list was uploaded successfully']

    # render the page
    return render(request, 'bed_maker/manual_import.html', context)