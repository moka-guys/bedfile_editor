from django import forms
from .models import  BedfileRequest

from django.urls import reverse
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML


class ManualUploadForm(forms.Form):
    """
    Form for manually inputting data
    """

    pan_number = forms.CharField()
    date_requested = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'style':'max-width: 12em'}))
    requested_by = forms.CharField()
    gene_list = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super(ManualUploadForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'manual-upload-form'
        self.helper.label_class = 'col-lg-2' # Set from Crispy Form Template 
        self.helper.field_class = 'col-lg-10' # Set from Crispy Form Template 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Import', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            HTML('<br><h5>Bedfile Request</h5>'),
            Field('pan_number', placeholder="Enter new Pan number for this panel"),
            Field('date_requested', placeholder="Enter date Panel requested" ),
            Field('requested_by', placeholder="Enter requester's name"),
            HTML('<br><h5>Ensembl Gene List</h5>'),
            Field('gene_list', placeholder="Enter Ensembl Gene IDs beginning ENSG i.e.\nENSG00000012048\nENSG00000141510\nENSG00000146648"),
            HTML('<br>Sample set:<br>ENSG00000012048<br>ENSG00000141510<br>ENSG00000146648'), 
            HTML('<p id="p1"></p>'),    
        )   
