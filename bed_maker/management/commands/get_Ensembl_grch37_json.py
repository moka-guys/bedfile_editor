from bed_maker.externalAPIs import create_grch37_json
import django
django.setup()

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''
    Create json file with grch37 gene data.
    '''

    help = 'This command creates a json file from a csv file located in the Ensembl_grch37 folder. Please refer to the function create_grch37_json for more infomration.'
    
    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str)

    def handle(self, *args, **kwargs):

        create_grch37_json()