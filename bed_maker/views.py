from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import ManualUploadForm
from .models import *
import datetime

# Create your views here.
def home(request):
    return render(request, 'bed_maker/home.html', {})


def view(request):
    return render(request, 'bed_maker/view.html', {})


def manual_import(request):
    import_form = ManualUploadForm()

    context = {'import_form': import_form,}
    

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
            # Get Gene list
            gene_list = [y for y in (x.strip() for x in cleaned_data['gene_list'].splitlines()) if y]
            for gene_ID in gene_list:
                gene= Gene.objects.create(
                ensembl_gene_id = gene_ID,
                bedfile_request_id = bedfile_request,
            ) 
            
    
    return render(request, 'bed_maker/manual_import.html', context)