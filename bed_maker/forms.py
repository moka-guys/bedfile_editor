from django import forms
from .models import  BedfileRequest


class ManualUploadForm(forms.Form):
    """
    """

    pan_number = forms.CharField()
    date_requested = forms.DateField()
    requested_by = forms.CharField()
    