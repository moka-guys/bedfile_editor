from django import forms
from bed_maker.models import  BedfileRequest

from django.urls import reverse
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Row, Column



class BedfileExportForm(forms.Form):
    """
    Form for exporting bedfiles
    """
    select_bedfile_request = forms.ModelChoiceField(required=True, widget=forms.Select, queryset=BedfileRequest.objects.all())

    select_bedfile_format = forms.ChoiceField(
    choices = (
        ('Standard Bedfile', "Create Standard Bedfile for variant calling"), 
        ('RPKM Bedfile', "Create RPKM BedFile for calculating coverage"),
    ),
    widget = forms.RadioSelect,
    initial = 'Standard Bedfile',
     label='Select the Bed Format',
    )
    
    def __init__(self, *args, **kwargs):
        super(BedfileExportForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'bedfile-export-form'
        self.helper.label_class = 'col-lg-2' # Set from Crispy Form Template 
        self.helper.field_class = 'col-lg-10' # Set from Crispy Form Template 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Export Bedfile', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
        Field('select_bedfile_request', label='Select Bedfile Request to Export'),
        Field('select_bedfile_format', label='Select Output BED file format'),
                    )