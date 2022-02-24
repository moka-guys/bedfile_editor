from bed_maker.externalAPIs import get_panel_app_list
from bed_maker.models import PanelAppList
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
        panelApp_df = get_panel_app_list()
        # Convert pandas dataframe to dictionary of records to reiterate over
        df_records = panelApp_df.to_dict('records')

        # Import to database
        for record in df_records:
            panelapplist = PanelAppList.objects.get_or_create(
                id = record['id'],
                name = record['name'],
                hash_id = record['hash_id'],
                version = record['version'],
                disease_sub_group = record['disease_sub_group'],
                relevant_disorders = record['relevant_disorders'],
                signed_off = record['signed_off'],
                number_of_genes = record['stats.number_of_genes'],
                number_of_regions = record['stats.number_of_regions'],
            )


