from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import ManualUploadForm
from .models import *
import datetime
import requests, sys
import pandas as pd

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from bed_maker.forms import SignUpForm, AccountAuthenticationForm
from bed_maker.tockens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login, logout

# Create your views here.
def home(request):
    return render(request, 'bed_maker/home.html', {})

def view(request):
    """
    View a list of transcripts
    """
    transcript_list = Transcript.objects.all()

    return render(request, 'bed_maker/view.html', {'transcripts': transcript_list})

def get_MANE_list():
    '''
    Get a JSON of MANE transcripts via the TARK API and return it as a Pandas Dataframe.
    MANE transcripts are minimal set of matching RefSeq and Ensembl transcripts of human
    protein-coding genes, where the transcripts from a matched pair are identical
    (5’ UTR, coding region and 3’ UTR), but retain their respective identifiers.

    The MANE transcript set is classified into two groups:

    1) MANE Select: One high-quality representative transcript per protein-coding gene that is well-supported by 
    experimental data and represents the biology of the gene.
    2) MANE Plus Clinical: Transcripts chosen to supplement MANE Select when needed for clinical variant reporting.
    '''
    server = "http://dev-tark.ensembl.org"

    ext = f"/api/transcript/manelist/"
    
    r = requests.get(server+ext, headers={ "Content-Type" : "text/html"})
    
    # Send informative error message if bad request returned 
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    
    decoded = r.json()
    # ens_stable_id, ens_stable_id_version, refseq_stable_id, refseq_stable_id_version, mane_type, ens_gene_name
    MANE_list_df = pd.DataFrame(decoded) 
    
    return(MANE_list_df)  

def lookup_ensembl_gene(ensembl_gene_id):
    '''
    Get transcripts related to Ensembl Gene ID from the Ensembl REST API
    '''
    server = "https://rest.ensembl.org"

    ext = f"/lookup/id/{ensembl_gene_id}?expand=1&utr=1"
    
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    
    # Send informative error message if bad request returned 
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    
    decoded = r.json()
    return(decoded)

def manual_import(request):
    """
    Takes the input from the manual input form and imports it into the database
    """
    # setup view
    import_form = ManualUploadForm()

    context = {'import_form': import_form,}
    
    # if form is submitted
    if request.method == 'POST':

        import_form = ManualUploadForm(request.POST)
        if import_form.is_valid:
            print(import_form)
            cleaned_data = import_form.cleaned_data

           # get bedfile request data - BedfileRequest is created when the users fills in
           # the Import details in the webapp creating a BedfileRequest object which is defined in models.py
            bedfile_request, created = BedfileRequest.objects.get_or_create(
                pan_number = cleaned_data['pan_number'],
                date_requested = cleaned_data['date_requested'],
                requested_by = cleaned_data['requested_by'],
                request_status = 'draft',
            )

            # Use the TARK API to get most recent version of the MANE transcript list

            MANE_list_df = get_MANE_list()

            # Get Gene list - Gene objects is defined in models.py - it populates the data into the 
            # genes table for every BedfileRequest made.
            # List comprehension to split lines input by user into a list and trim any white space
            gene_list = [y for y in (x.strip() for x in cleaned_data['gene_list'].splitlines()) if y]
            for gene_ID in gene_list:
                gene = Gene.objects.create(
                ensembl_gene_id = gene_ID,
                bedfile_request_id = bedfile_request,
                )
                # Populate database with transcript details for each gene using Ensembl API
                gene_object = lookup_ensembl_gene(gene_ID)
                for transcript_dict in gene_object["Transcript"]:
                    # check if the Transcript ID is present in a list of all MANE transcripts, if it does it allocates True to the field MANE_transcript 
                    # and adds the appropriate RefSeq ID to the field
                    if transcript_dict["id"] in MANE_list_df.ens_stable_id.values:
                        MANE_transcript = 'True'
                        RefSeq_transcript_id = MANE_list_df.loc[MANE_list_df['ens_stable_id'] == transcript_dict["id"]]['refseq_stable_id'].item()
                    else:
                        MANE_transcript = 'False'
                        RefSeq_transcript_id = ''
                    transcript = Transcript.objects.create(
                    ensembl_transcript_id = transcript_dict["id"],
                    bedfile_request_id = bedfile_request,
                    gene_id = gene,
                    display_name = transcript_dict["display_name"],
                    start = transcript_dict["start"],
                    end = transcript_dict["end"],
                    MANE_transcript = MANE_transcript,
                    RefSeq_transcript_id = RefSeq_transcript_id
                    )
            # add success message to page
            context['message'] = ['Gene list was uploaded successfully']

    # render the page
    return render(request, 'bed_maker/manual_import.html', context)


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        signup_form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def logout_view(request):
	logout(request)
	return redirect("home")


def login_view(request, *args, **kwargs):
	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("bed_maker/home")

	destination = get_redirect_if_exists(request)
	print("destination: " + str(destination))

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				if destination:
					return redirect(destination)
				return redirect("bed_maker/home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "registration/login.html", context)

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


