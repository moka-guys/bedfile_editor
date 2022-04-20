from bed_maker.externalAPIs import download_ensembl_annotations
import django
django.setup()

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''
    Download Ensembl Gene Annotations for grch38, approximately 3GB.
    '''

    help = 'This command Downloads Ensembl Gene Annotations'
    
    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str)

    def handle(self, *args, **kwargs):

        download_ensembl_annotations()