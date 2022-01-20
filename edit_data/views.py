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
    # setup view
    selected_form = BedfileSelectForm()
    
    context = {'selected_form': selected_form,}
    
    # if form is submitted
    if request.method == 'POST':

        selected_form = BedfileSelectForm(request.POST)
        if selected_form.is_valid:
            print(selected_form)
            cleaned_data = selected_form.cleaned_data
            selected_bedfile_request = cleaned_data['select_bedfile_request']          
    # render the page
    return render(request, 'bed_maker/edit.html', context)
