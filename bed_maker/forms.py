from django import forms
from .models import  BedfileRequest, Profile

from django.urls import reverse
from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
        )   


class SignUpForm(UserCreationForm):
    email                   = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Profile
        fields = ('email', 'password1', 'password2', )
    
    def clean_email(self):
	    email = self.cleaned_data['email'].lower()
	    try:
		    account = Profile.objects.exclude(pk=self.instance.pk).get(email=email)
	    except User.DoesNotExist:
		    return email
	    raise forms.ValidationError('Email "%s" is already in use.' % account)

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Profile
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")
