from bed_maker.externalAPIs import download_Clinvar_data
import django
django.setup()

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''
    Download clinvar data to calculate clinvar overage for each transcript
    '''

    help = 'Downaload Clinvar Data, this command will remove current Clivar directory and create a new one with the same name'
    
    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str)

    def handle(self, *args, **kwargs):

        download_Clinvar_data()