from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
def home(request):
    return render(request, 'bed_maker/home.html', {})


def view(request):
    return render(request, 'bed_maker/view.html', {})


def manual_import(request):
    return render(request, 'bed_maker/manual_import.html', {})