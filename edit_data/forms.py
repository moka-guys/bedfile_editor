from django import forms
from bed_maker.models import  BedfileRequest

from django.urls import reverse
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Row, Column
from crispy_forms.bootstrap import Accordion, AccordionGroup


class BedfileSelectForm(forms.Form):
    """
    Form for selecting bedfiles
    """
    select_bedfile_request = forms.ModelChoiceField(required=True, queryset=BedfileRequest.objects.all(), initial=0)

    def __init__(self, *args, **kwargs):
        super(BedfileSelectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'bedfile-select-form'
        self.helper.label_class = 'col-lg-2' # Set from Crispy Form Template 
        self.helper.field_class = 'col-lg-10' # Set from Crispy Form Template 
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Select BedfileRequest', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
        Field('select_bedfile_request', label='Select Bedfile Request to View/Edit'),
                    )
