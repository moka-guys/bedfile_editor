from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests, sys
from .forms import BedfileExportForm
from bed_maker.models import *
from pybedtools import BedTool
import pandas as pd
import mimetypes
import os

# Create your views here.
def ExportBedfile(request):
    """
    Provide List of BedfileRequests
    """
    # setup view
    export_form = BedfileExportForm()
    
    context = {'export_form': export_form,}
    
    # if form is submitted
    if request.method == 'POST':

        export_form = BedfileExportForm(request.POST)
        if export_form.is_valid:
            print(export_form)
            cleaned_data = export_form.cleaned_data
            selected_bedfile_request = cleaned_data['select_bedfile_request']
            selected_bedfile_format = cleaned_data['select_bedfile_format']
            # Return selected transcripts for specified BedfileRequest
            selected_transcript_queryset = Transcript.objects.filter(selected_transcript=True, bedfile_request_id__pan_number=str(selected_bedfile_request))
            df = pd.DataFrame.from_records(selected_transcript_queryset.values())
            export_df = df[['chromosome', 'start', 'end', 'ensembl_id']]
            # Define text file name
            bedfile_name = f'{str(selected_bedfile_request)}.bed'
            # Define Django project base directory
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # Define the full file path
            filepath = BASE_DIR + '/bedfile_output/' + bedfile_name
            temp_bedfile = BedTool.from_dataframe(export_df).moveto(filepath)
            # Open the file for reading content
            path = open(filepath, 'r')
            # Set the mime type
            mime_type, _ = mimetypes.guess_type(filepath)
            # Set the return value of the HttpResponse
            response = HttpResponse(path, content_type=mime_type)
            # Set the HTTP header for sending to browser
            response['Content-Disposition'] = "attachment; filename=%s" % bedfile_name
            # Return the response value
            return response
    # render the page
    return render(request, 'bed_maker/export.html', context)

