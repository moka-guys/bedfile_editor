from unicodedata import name
from django.db import models
from importlib_metadata import version
import textwrap
import re

# Create your models here.

class BedfileRequest(models.Model):
    """
    Model to store bedfile request details
    """
    bedfile_request_id = models.AutoField(primary_key=True)
    pan_number = models.CharField(max_length=10)
    date_requested = models.DateField()
    requested_by = models.CharField(max_length=20)
    request_status = models.CharField(max_length=10, choices=(('draft', 'draft'), ('published', 'published'), ('deprecated', 'deprecated')))
    request_transcript_padding = models.IntegerField(default=0)
    request_introns = models.BooleanField(default=False)
    request_exon_padding = models.IntegerField(default=False)
    request_five_prime_UTR= models.BooleanField(default=False)
    request_three_prime_UTR= models.BooleanField(default=False)
    request_five_prime_UTR_padding = models.IntegerField(default=0)
    request_three_prime_UTR_padding = models.IntegerField(default=0)
    panel_category = models.CharField(max_length=25, default="")
    panel_subcategory = models.CharField(max_length=25, default="")
    panel_name = models.CharField(max_length=25, default="")

    def __str__(self):
        return f'{self.pan_number}'

class Gene(models.Model):
    """
    Model to store gene details
    """
    gene_id = models.AutoField(primary_key=True)
    # ensembl gene ID begining ENSG
    display_name = models.CharField(max_length=15, default="placeHolder")
    ensembl_id = models.CharField(max_length=15)
    bedfile_request_id = models.ForeignKey('BedfileRequest', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ensembl_id}'

class Transcript(models.Model):
    """
    Model to store transcript details
    """
    transcript_id = models.AutoField(primary_key=True)
    # ensembl transcript ID begining ENST
    ensembl_id = models.CharField(max_length=15)
    ensembl_transcript_version = models.CharField(max_length=3, default="")
    # RefSeq transcript ID begining NM
    RefSeq_transcript_id = models.CharField(max_length=15)
    RefSeq_transcript_version = models.CharField(max_length=3, default="")
    bedfile_request_id = models.ForeignKey('BedfileRequest', on_delete=models.CASCADE,)
    gene_id = models.ForeignKey('Gene', on_delete=models.CASCADE,  related_name='gene_transcripts',)
    chromosome=models.CharField(max_length=2)
    display_name = models.CharField(max_length=15)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    coverage = models.CharField(max_length=50)
    MANE_transcript = models.BooleanField()
    RefSeq_HGMD_transcript = models.BooleanField(default=False)
    biotype = models.CharField(max_length=50, default="")
    recommended_transcript = models.BooleanField(default=False)
    selected_transcript = models.BooleanField(default=False)
    transcript_padding = models.IntegerField(default=0)
    include_introns = models.BooleanField(default=False)
    include_exon_padding = models.IntegerField(default=False)
    include_five_prime_UTR= models.BooleanField(default=False)
    include_three_prime_UTR= models.BooleanField(default=False)
    five_prime_UTR_padding = models.IntegerField(default=0)
    three_prime_UTR_padding = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.ensembl_id}'

class Exon(models.Model):
    """
    Model to store exon details
    """
    exon_id = models.AutoField(primary_key=True)
    # ensembl transcript ID begining ENST
    ensembl_id = models.CharField(max_length=15)
    ensembl_exon_version = models.CharField(max_length=3, default="")
    chromosome=models.CharField(max_length=2)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    bedfile_request_id = models.ForeignKey('BedfileRequest', on_delete=models.CASCADE,)
    gene_id = models.ForeignKey('Gene', on_delete=models.CASCADE,  related_name='gene_exons',)
    transcript_id = models.ForeignKey('Transcript', on_delete=models.CASCADE,)

    def __str__(self):
        return f'{self.ensembl_id}'

class UTR(models.Model):
    """
    Model to store UTR details
    """
    utr_id = models.AutoField(primary_key=True)
    # ensembl transcript ID begining ENST
    ensembl_id = models.CharField(max_length=15)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    bedfile_request_id = models.ForeignKey('BedfileRequest', on_delete=models.CASCADE,)
    gene_id = models.ForeignKey('Gene', on_delete=models.CASCADE,  related_name='gene_utrs',)
    transcript_id = models.ForeignKey('Transcript', on_delete=models.CASCADE,)
    utr_type = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.ensembl_id}'

class GenomicRange(models.Model):
    """
    Model to store genomic ranges for user specified regions
    """
    genomic_range_id = models.AutoField(primary_key=True)
    bedfile_request_id = models.ForeignKey('BedfileRequest', on_delete=models.CASCADE,)
    # genomic range info
    genomic_region_id=models.CharField(max_length=15)
    chromosome=models.CharField(max_length=2)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.genomic_region_id}'

class PanelAppList(models.Model):
    """
    Model to Panel App Panel Details
    """
    Panel_app_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    hash_id = models.CharField(max_length=25)
    version = models.CharField(max_length=11)
    disease_sub_group = models.CharField(max_length=50)
    relevant_disorders = models.CharField(max_length=100)
    signed_off = models.DateField()
    number_of_genes = models.IntegerField()
    number_of_regions = models.IntegerField()

    def __str__(self):
        # Clean up relevant_orders to return only R number/s
        r = re.compile("R[0-9]+")
        readable_description = f'{", ".join(re.findall(r, self.relevant_disorders))}, {self.name}'
        readable_description = readable_description.strip(', ')
        return readable_description

class HGNC2ensembl(models.Model):
    """
    Model to Panel App Panel Details
    """
    id = models.AutoField(primary_key=True)
    HGNC_id = models.CharField(max_length=10)
    HGNC_symbol = models.CharField(max_length=10)
    ensembl_id = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.HGNC_id}, {self.HGNC_symbol}, {self.ensembl_id}'

class ClinvarCoverage_grch37(models.Model):
    """
    Model to Clinvar Coverage
    """
    transcript_ensembl_id = models.CharField(max_length=15)
    clinvar_coverage_fraction = models.CharField(max_length=20)
    clinvar_variants = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.transcript_ensembl_id}'

class ClinvarCoverage_grch38(models.Model):
    """
    Model to Clinvar Coverage
    """
    transcript_ensembl_id = models.CharField(max_length=15)
    clinvar_coverage_fraction = models.CharField(max_length=20)
    clinvar_variants = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.transcript_ensembl_id}'