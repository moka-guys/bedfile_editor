# Functions to interact wwith the Ensmbl API 

import requests, sys

def lookup_ensembl_gene(ensembl_gene_id):
    server = "https://rest.ensembl.org"

    ext = f"/lookup/id/{ensembl_gene_id}?expand=1&utr=1"
    
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    
    decoded = r.json()
    return(decoded)
