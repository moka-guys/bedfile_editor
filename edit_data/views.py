from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests, sys
from .forms import BedfileSelectForm
from bed_maker.models import *

# def edit(request):
#     """
#     Edit Bedfile requests
#     """
#     transcript_list = Transcript.objects.all()

#     return render(request, 'bed_maker/edit.html', {'transcripts': transcript_list})

# Create your views here.

def SelectBedfile(request):
    """
    Provide List of BedfileRequests
    """
    
    # if form is submitted
    if request.method == 'POST':
        form = BedfileSelectForm(request.POST)

        if form.is_valid():
            try:
                selected_bedfile_request = form.cleaned_data['select_bedfile_request'].pk    
                gene_data_api_url = f"/api/v1/genes/?format=json&bedfile_request_id={selected_bedfile_request}"
                print(gene_data_api_url)
                context = {'selected_form': form, 'gene_data_api_url' : gene_data_api_url}
                return render(request, 'bed_maker/edit.html', context)

            except ValueError as e:
                print(e)
                context = {'selected_form': form, 'gene_data_api_url' : "/api/v1/genes/?format=json"}
                return render(request, 'bed_maker/edit.html', context)
        context = {'selected_form': form, 'gene_data_api_url' : "/api/v1/genes/?format=json"}
        return render(request, 'bed_maker/edit.html', context)
    else:
        form = BedfileSelectForm(request.POST)
        context = {'selected_form': form, 'gene_data_api_url' : "/api/v1/genes/?format=json"}
        return render(request, 'bed_maker/edit.html', context)