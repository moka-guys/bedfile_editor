from django import forms
from .models import  BedfileRequest

from django.urls import reverse
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Row, Column
from crispy_forms.bootstrap import Accordion, AccordionGroup


class ManualUploadForm(forms.Form):
    """
    Form for manually inputting data
    """

    pan_number = forms.CharField(label = "Pan Number")
    date_requested = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'style':'max-width: 12em'}))
    requested_by = forms.CharField(label = "Requested By")
    gene_list = forms.CharField(widget=forms.Textarea)
    request_transcript_padding = forms.IntegerField(label = "Transcript Padding?")
    request_introns = forms.BooleanField(label = "Include Introns?", initial=False, required=False)
    request_exon_padding = forms.IntegerField(label = "Exon Padding")
    request_five_prime_UTR= forms.BooleanField(label = "Include 5' UTR", initial=False, required=False)
    request_three_prime_UTR= forms.BooleanField(label = "Include 3' UTR", initial=False, required=False)
    request_five_prime_UTR_padding = forms.IntegerField(label = "5' UTR Padding", widget=forms.TextInput(attrs={'style':'max-width: 20em'}),)
    request_three_prime_UTR_padding = forms.IntegerField(label = "3' UTR Padding", widget=forms.TextInput(attrs={'style':'max-width: 20em'}),)
    panel_category = forms.CharField()
    panel_subcategory = forms.CharField()
    panel_name = forms.CharField()
    
    genome_ref_select = forms.ChoiceField(
    choices = (
        ('GRCh38', "GRCh38"), 
        ('GRCh37', "GRCh37"),
    ),
    widget = forms.RadioSelect,
    initial = 'GRCh38',
    )

    region_list = forms.CharField(widget=forms.Textarea, initial="", required=False)
    
    bedfile_select = forms.ChoiceField(
    choices = (
        ('Standard Bedfile', "Create Standard Bedfile for variant calling"), 
        ('RPKM Bedfile', "Create RPKM BedFile for calculating coverage"),
    ),
    widget = forms.RadioSelect,
    initial = 'Standard Bedfile',
    )
    
    def __init__(self, *args, **kwargs):
        super(ManualUploadForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'manual-upload-form'
        self.helper.label_class = 'col-lg-2' # Set from Crispy Form Template 
        self.helper.field_class = 'col-lg-10' # Set from Crispy Form Template 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Request', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
    
            Accordion(
                AccordionGroup('Bedfile Request & Gene List',
                    Field('pan_number', placeholder="Enter new Pan number for this panel"),
                    HTML('<br><h5>Panel Description</h5>'),
                    Field('panel_category', placeholder="Enter Panel Category"),
                    Field('panel_subcategory', placeholder="Enter Panel Subcategory"),
                    Field('panel_name', placeholder="Enter Panel Name"),
                    Field('date_requested', placeholder="Enter date Panel requested" ),
                    Field('requested_by', placeholder="Enter requester's name"),                         
                    HTML('<br><h5>Enter Ensembl Gene List</h5>'),
                    Field('gene_list', placeholder="Enter Ensembl Gene IDs beginning ENSG i.e.\nENSG00000012048\nENSG00000141510\nENSG00000146648"),
                    HTML('<br>Sample set:<br>ENSG00000012048<br>ENSG00000141510<br>ENSG00000146648<br>'),
                ),
                AccordionGroup('Select Untranslated Regions & Set Padding',
                    Row(
                        Column(Field('request_exon_padding', value=0)),
                        ),
                    Row(
                        Field('request_introns', placeholder="Should Introns be included"),
                    ),
                        Row(
                        Column(Field('request_five_prime_UTR', placeholder="Include 5' UTR")),
                        Column(Field('request_five_prime_UTR_padding', value=0)),
                        ),
                        Row(
                        Column(Field('request_three_prime_UTR', placeholder="Include 3' UTR")),
                        Column(Field('request_three_prime_UTR_padding', value=0)),
                    ),
                ),
                AccordionGroup('Manually Enter Genomic Regions',
                            Field('genome_ref_select'),
                            Field('region_list', placeholder="Enter additional genomic regions (ID,Chr,Start,End)\nRegion1,3,100000,200000 \nRegion2,11,180000,200000"),
                    )
            ),
        )
