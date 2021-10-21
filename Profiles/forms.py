from django import forms
from Profiles.models import  Profile


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignUpForm(UserCreationForm):
    email                   = forms.EmailField(max_length=250, required=True, help_text='Required. Provide a valid email address.')
    first_name              = forms.CharField(max_length=50, required=True, help_text='Required. Enter first name')
    last_name               = forms.CharField(max_length=50, required=True, help_text='Required. Enter last name')
    
    class Meta:
        model = Profile
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )
    
    def clean_email(self):
	    email = self.cleaned_data['email'].lower()
	    try:
		    account = Profile.objects.exclude(pk=self.instance.pk).get(email=email)
	    except:
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

