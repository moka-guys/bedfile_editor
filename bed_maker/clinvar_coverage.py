import vcf
import requests
import sys, os
import pandas as pd
from config.settings import BASE_DIR

cur_path = BASE_DIR
'''
Get path to Clinvar folder to calculate Clinvar Coverage
'''

def download(url: str, dest_folder: str):
    '''
    Download function for Clinvar vcf files if not already present
    '''
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

if os.path.exists(cur_path + '/Clinvar'):
    pass
else:
    os.mkdir(cur_path + '/Clinvar')

if os.path.exists(cur_path + '/Clinvar/clinvar.vcf.gz'):
    pass
else: 
    download("https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz", dest_folder=cur_path+"/Clinvar")
if os.path.exists(cur_path + '/Clinvar/clinvar.vcf.gz.tbi'):
    pass
else:
    download("https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi", dest_folder=cur_path+"/Clinvar")

vcfReader = vcf.Reader(filename=cur_path+'/Clinvar/clinvar.vcf.gz', compressed=True)

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

def get_transcript_intervals(transcript): 
    '''
    Get a list of chromosomal coordinates for the exons
    '''
    intervals = []
    for Exon in transcript['Exon']:
        chr = Exon['seq_region_name']
        start = Exon['start']
        end = Exon['end']
        interval = (chr,start,end)
        intervals.append(interval)
    return intervals

def get_variants(intervals):
    '''
    Get the list of variants for the exon regions of each transcript
    '''
    result = set()
    for interval in intervals:
        chrom, start, end = interval
        for v in vcfReader.fetch(chrom,start,end):
            result.add(v.ID)  
    return list(result)

def annotate_transcripts(gene_data):
    '''
    Annotate the transcripts with information, such as Clivar Coverage,
    if MANE transcript and get the corresponding transcript RefSeq ID.
    '''
    transcripts = []
    MANE_list_df = get_MANE_list()
    ClinvarDetails = vcfReader.metadata['fileDate'] + ' ' + vcfReader.metadata['reference']

    for transcript in gene_data['Transcript']:
        if transcript["id"] in MANE_list_df.ens_stable_id.values:
            MANE_transcript = 'True'
            RefSeq_transcript_id = MANE_list_df.loc[MANE_list_df['ens_stable_id'] == transcript["id"]]['refseq_stable_id'].item()
        else:
            MANE_transcript = 'False'
            RefSeq_transcript_id = ''            

        transcript_intervals = get_transcript_intervals(transcript)
            # exclude haplotypes (as not in clinvar)
        transcript_intervals = list([ i for i in transcript_intervals if 'hap' not in i[0] ])
            # build result dict
        transcripts.append({
            'id': transcript['id'],
            'display_name' : transcript['display_name'],
            'variants': get_variants(transcript_intervals) if transcript_intervals else [],
            'coding': bool(transcript_intervals),
            'clinvar_details': ClinvarDetails,
            'MANE_transcript': MANE_transcript,
            'RefSeq_transcript_id': RefSeq_transcript_id,
            'start': transcript["start"],
            'end' : transcript["end"]
        })
    # count gene variants and update covered clinvar fraction
    gene_variants = set([ variant for t in transcripts for variant in t['variants'] ])
    for tx in transcripts:
        if gene_variants:
            tx['coverage'] = len(tx['variants'])/len(gene_variants)
            tx['clinvar_coverage'] = round(tx["coverage"]*100, 1) if tx["coverage"] else None
            tx['clinvar_variants'] = len(tx["variants"]),
        else:
            tx['coverage'] = None
    return transcripts