import vcf
import requests
import sys, os
import pandas as pd


def lookup_ensembl_gene(ensembl_id):
    '''
    Get transcripts related to Ensembl Gene ID from the Ensembl REST API
    '''
    server = "https://rest.ensembl.org"

    ext = f"/lookup/id/{ensembl_id}?expand=1&utr=1"
    
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    
    # Send informative error message if bad request returned 
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    
    decoded = r.json()
    return(decoded)

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

MANE_list_df = get_MANE_list()

gene_ID = "ENSG00000146648"
bedfile_request = "Pan111"
display_name = 'placeholder'

def process_ensembl_gene_data(gene_ID):

    #Get data for gene from ensembl API
    ensembl_gene_data = lookup_ensembl_gene(gene_ID)

    # Get Gene level data
    print(gene_ID)
    print(bedfile_request)
    print(ensembl_gene_data["display_name"])
    print(ensembl_gene_data["version"])
    print(ensembl_gene_data["biotype"])
    print(ensembl_gene_data["seq_region_name"])
    
    # Get Transcript level data
    for transcript in ensembl_gene_data["Transcript"]:
        print("    ",transcript['id'])
        print("    ",transcript['seq_region_name'])
        print("    ",transcript['start'])
        print("    ",transcript['end'])
        print("    ",transcript['is_canonical'])
        print("    ",transcript['biotype'])

        # Get UTR level data for transcript
        for utr in transcript["UTR"]:
            print("        ", utr['id'])
            print("            ", utr['type'])
            print("            ", utr['seq_region_name'])
            print("            ", utr['start'])
            print("            ", utr['end'])
        # Get Exon level data for transcript
        for exon in transcript["Exon"]:
            print("                ", exon["id"])
            print("                    ", exon["version"])
            print("                    ", exon['seq_region_name'])
            print("                    ", exon["start"])
            print("                    ", exon["end"])


process_ensembl_gene_data(gene_ID)

