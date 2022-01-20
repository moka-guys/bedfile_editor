from django.urls import path
from .views import ExportBedfile

urlpatterns = [
    path('', ExportBedfile, name='export'),
]