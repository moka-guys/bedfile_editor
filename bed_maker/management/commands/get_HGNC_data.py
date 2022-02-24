from bed_maker.externalAPIs import get_HGNC_data
from bed_maker.models import HGNC2ensembl
import django
django.setup()

from django.core.management.base import BaseCommand, CommandError
import pandas as pd

class Command(BaseCommand):
    '''
    Placeholder
    '''

    help = 'Import list of PanelAp panels listed via the PanelApp API'
    
    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str)

    def handle(self, *args, **kwargs):

        # Import data from Panel App API
        df = get_HGNC_data()
        # Convert pandas dataframe to dictionary of records to reiterate over
        df_records = df.to_dict('records')

        # Import to database TODO look at optimizing as current method extremely slow
        for record in df_records:
            print(record)
            hgncensembl = HGNC2ensembl.objects.get_or_create(
                HGNC_id = record['HGNC_id'],
                HGNC_symbol = record['HGNC_symbol'],
                ensembl_id = record['ensembl_id'],
            )


