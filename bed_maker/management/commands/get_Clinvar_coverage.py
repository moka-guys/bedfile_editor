from bed_maker.externalAPIs import calculate_clinvar_coverage_for_all_ensembl_transcripts
import django
django.setup()

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''
    Calculate Clinvar Coverage for all ensembl transcripts
    '''

    help = 'Calculate Clinvar Coverage'
    
    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str)

    def handle(self, *args, **kwargs):

        calculate_clinvar_coverage_for_all_ensembl_transcripts()