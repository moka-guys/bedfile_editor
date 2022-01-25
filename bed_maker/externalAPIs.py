import vcf
import requests
import sys, os
import pandas as pd
import pickle
from collections import Counter
from config.settings import BASE_DIR

cur_path = BASE_DIR

'''
Get path to Clinvar folder to calculate Clinvar Coverage
'''
# TODO check if this function is actially used
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



def get_MANE_list():
    '''
    Get a JSON of MANE transcripts via the TARK API and return it as a Pandas Dataframe.
    MANE transcripts are minimal set of matching RefSeq and Ensembl transcripts of human
    protein-coding genes, where the transcripts from a matched pair are identical
    (5’ UTR, coding region and 3’ UTR), but retain their respective identifiers.
    The MANE data is cached locally for speed and reliability.

    The MANE transcript set is classified into two groups or mane_type:

    1) MANE Select: One high-quality representative transcript per protein-coding gene that is well-supported by 
    experimental data and represents the biology of the gene.
    2) MANE Plus Clinical: Transcripts chosen to supplement MANE Select when needed for clinical variant reporting.
    
    :return: pandas dataframe containing the MANE data with the following columns "ens_stable_id", "ens_stable_id_version", "refseq_stable_id", "refseq_stable_id_version", "mane_type", "ens_gene_name"
    :rtype: pandas dataframe
    '''
    cur_path = BASE_DIR

    # Check whether there is a cached MANE list CSV file that can be used (improves speed and reliability)
    if os.path.isfile(cur_path+'/external_data/MANElist.csv'):
        MANE_list_df = pd.read_csv(cur_path + '/external_data/MANElist.csv',)
    else:
    # if no cache download MANE list from TARK API
        server = "http://dev-tark.ensembl.org"

        ext = f"/api/transcript/manelist/"
        r = requests.get(server+ext, headers={ "Content-Type" : "text/html"})
        
        # Send informative error message if bad request returned 
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        
        decoded = r.json()
        # df columns: ens_stable_id, ens_stable_id_version, refseq_stable_id, refseq_stable_id_version, mane_type, ens_gene_name
        MANE_list_df = pd.DataFrame(decoded) 
        # Cache MANE list for future use to improve speed and reliability
        MANE_list_df.to_csv(cur_path + '/external_data/MANElist.csv', index=False,  encoding='utf-8')
    return(MANE_list_df)  


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

def get_transcript_intervals(transcript): 
    '''
    Gets a list of chromosomal coordinates for the exons and UTRs composing a single transcript obtained from the Ensembl API

    :param transcript: A dictionary of data related to an Ensembl transcript imported via the ensembl API, including all Exons and UTRs for that transcript
    :type transcript: dictionary of dictionaries, required
    :return: Intervals, a list of tuples (chr,start,end)
    :rtype: list of tuples 
    '''
    intervals = []
    for Exon in transcript['Exon']:
        chr = Exon['seq_region_name']
        start = Exon['start']
        end = Exon['end']
        interval = (chr,start,end)
        intervals.append(interval)
    if 'UTR' in transcript.keys():
        for UTR in transcript['UTR']:
            chr = UTR['seq_region_name']
            start = UTR['start']
            end = UTR['end']
            interval = (chr,start,end)
            intervals.append(interval)
    return intervals

def count_clinvar_variants_per_gene(variant_type=['All'], clinical_significance=['All']):
    '''
    Count the number of variants per gene symbol in a VCF file containing variants from the Clinvar database

    :para variant_type: List of variant types to include in count for each gene, any other variant types are filtered out, if omitted all variant types returned. Example varinat types: 'single_nucleotide_variant', 'copy_number_gain', 'copy_number_loss', 'Deletion', 'Duplication', 'Indel', 'Insertion', 'Inversion', 'Microsatellite', 'Variation'
    :type variant_type: list, optional
    :para clinical_significance: List of clinical significance terms used to filter variants for inclusion in count for each gene, if omitted all results returnd, Examples include 'Benign', 'Benign/Likely_benign', 'Likely_benign', 'Likely_pathogenic', 'Pathogenic', 'Pathogenic/Likely_pathogenic', 'Uncertain_significance' - for a full list look at the VCF
    :type clinical_significance:
    :return: Intervals, a list of tuples (chr,start,end)
    :rtype: list of tuples 
    '''
    cur_path = BASE_DIR
    
    # Get clinVar data
    vcfReader = vcf.Reader(filename=cur_path+'/Clinvar/clinvar.vcf.gz', compressed=True,  encoding="utf-8")

    gene_list = []
    for record in vcfReader:
        if 'GENEINFO' in  record.INFO.keys():
            # If both optional settings are used don't filter on variant type or clinical significance
            if variant_type == ['All'] and clinical_significance == ['All']:
               gene_list.append(record.INFO['GENEINFO'].split(':')[0]) 
            elif variant_type == ['All']:
            # Filter only on clinical significance
                if record.INFO['CLNSIG'] in clinical_significance :
                    gene_list.append(record.INFO['GENEINFO'].split(':')[0])
            elif clinical_significance == ['All']:
                # Filter only on variant type
                if record.INFO['variant_type'] in variant_type :
                    gene_list.append(record.INFO['GENEINFO'].split(':')[0])
            else:
                # Filter on both variant type and clinical significance
                if record.INFO['CLNVC'] in variant_type and record.INFO['CLNSIG'] in clinical_significance :
                    gene_list.append(record.INFO['GENEINFO'].split(':')[0])
    return Counter(gene_list)

def get_clinvar_variant_summary(variant_type=['All'], clinical_significance=['All']):
    '''Read in ClinVar data from either vcf (SLOW), or use previously pickled summary file if it exists'''
    # TODO Generalise function by adding file path as args and add support for periodic running so that uptodate data is used, chck if vcfReader should be passed as arg
    cur_path = BASE_DIR
    # Check whether there is a cached summary that can be used
    if os.path.isfile(cur_path+'/Clinvar/clinvar_variant_per_gene.pkl'):
        with open(cur_path+'/Clinvar/clinvar_variant_per_gene.pkl', 'rb') as inputfile:
            clinvar_variant_per_gene = pickle.load(inputfile)
    else:
        # If no cache read in ClinVar vcf
        vcfReader = vcf.Reader(filename=cur_path+'/Clinvar/clinvar.vcf.gz', compressed=True,  encoding="utf-8")
        clinvar_variant_per_gene = count_clinvar_variants_per_gene(variant_type, clinical_significance)
        # Save summary ClinVar data for faster loading next time
        with open(cur_path+'/Clinvar/clinvar_variant_per_gene.pkl', 'wb') as outputfile:
            pickle.dump(clinvar_variant_per_gene, outputfile)
    return clinvar_variant_per_gene


def get_HGMD_data():    
    '''
    Get a list of RefSeq HGMD transcripts, a subset of RefSeq Curated transcripts which have been annotated by the Human Gene Mutation Database. This track is only available on the human genomes hg19 and hg38. It is the most restricted RefSeq subset, targeting clinical diagnostics
    # TODO write doc string
    :return: list of RefSeq IDs 
    :rtype: list
    '''
    cur_path = BASE_DIR
    # Check whether there is a cached copy of the HGMD data
    if os.path.isfile(cur_path+'/external_data/RefSeqHGMDtranscripts.pkl'):
        with open(cur_path+'/external_data/RefSeqHGMDtranscripts.pkl', 'rb') as inputfile:
            HGMD_list = pickle.load(inputfile)
    else:
        # If no cached data get HGMD data from ucsc API    
        server = "http://api.genome.ucsc.edu"
        ext = f"/getData/track?genome=hg38;track=ncbiRefSeqHgmd"
        r = requests.get(server+ext, headers={ "Content-Type" : "text/html"})
        # Send informative error message if bad request returned 
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        HGMD_list=[]
        for key in decoded['ncbiRefSeqHgmd'].keys():
            for item in decoded['ncbiRefSeqHgmd'][key]:
                HGMD_list.append(item['name'])
        # Save summary ClinVar data for faster loading next time
        with open(cur_path+'/external_data/RefSeqHGMDtranscripts.pkl', 'wb') as outputfile:
            pickle.dump(HGMD_list, outputfile)
    return(HGMD_list)

def get_variants_by_interval(intervals, variant_type=['All'], clinical_significance=['All']):
    '''
    Get the list of the specified variants for the exon regions of each transcript

    #TODO Add interval details
    :para variant_type: List of variant types to include, any other variant types are filtered out, if omitted all variant types returned. Example varinat types: 'single_nucleotide_variant', 'copy_number_gain', 'copy_number_loss', 'Deletion', 'Duplication', 'Indel', 'Insertion', 'Inversion', 'Microsatellite', 'Variation'
    :type variant_type: list, optional
    :para clinical_significance: List of clinical significance terms to include in output, if omitted all results returned, Examples include 'Benign', 'Benign/Likely_benign', 'Likely_benign', 'Likely_pathogenic', 'Pathogenic', 'Pathogenic/Likely_pathogenic', 'Uncertain_significance' - for a full list look at the VCF
    :type clinical_significance:
    :return: List of variants
    :rtype: list
    '''
    cur_path = BASE_DIR
    vcfReader = vcf.Reader(filename=cur_path+'/Clinvar/clinvar.vcf.gz', compressed=True,  encoding="utf-8")
    result = set()
    for interval in intervals:
        chrom, start, end = interval
        for record in vcfReader.fetch(chrom,start,end):
            if variant_type == ['All'] and clinical_significance == ['All']:
               result.add(record.ID)
            elif variant_type == ['All']:
            # Filter only on clinical significance
                if record.INFO['CLNSIG'] in clinical_significance:
                    result.add(record.ID)
            elif clinical_significance == ['All']:
                # Filter only on variant type
                if record.INFO['CLNVC'] in variant_type:
                    result.add(record.ID)
            else:
                # Filter on both variant type and clinical significance
                if record.INFO['CLNVC'] in variant_type and record.INFO['CLNSIG'] in clinical_significance :
                    result.add(record.ID)
    return list(result)

def calculate_clinvar_coverage_for_all_ensembl_transcripts():
    '''
    Pre-calculate the clinvar coverage for all Ensembl transcripts 
    # TODO Elaborate
    '''
    pass

def prioritise_transcripts(gene_id):
    '''
    Prioritise gene transcripts based upon Michael Yau's rule of 4
    TODO Clarify whether all known variants is limited to SNVs, and also Likely Pathogenic/Pathogenic
    | RULE1: RefSeq or MANE Select, and RefSeq HGMD 
    | RULE2: RefSeq or MANE Select, and covers all known ClinVar variants in gene
    | RULE3: RefSeq HGMD, and covers all known ClinVar variants in gene 
    | RULE4: Coding transcript (enables prioritisation of singleton transcripts)
    
    :return: String, Ensembl stable transcript ID 
    :rtype: str
    '''
    # TODO Write meaningful code here
    pass