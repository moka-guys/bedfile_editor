from django.db import models

# Create your models here.

class BedfileRequest(models.Model):
    """
    Model to store bedfile request details
    """
    bedfile_request_id = models.AutoField(primary_key=True)
    pan_number = models.CharField(max_length=10)
    date_requested = models.DateField()
    requested_by = models.CharField(max_length=20)
    request_status = models.CharField(max_length=10, choices=(('draft', 'draft'), ('published', 'published')))
    request_transcript_padding = models.IntegerField()
    request_introns = models.BooleanField()
    request_exon_padding = models.IntegerField()
    request_five_prime_UTR= models.BooleanField()
    request_three_prime_UTR= models.BooleanField()
    request_five_prime_UTR_padding = models.IntegerField()
    request_three_prime_UTR_padding = models.IntegerField()
    panel_category = models.CharField(max_length=25)
    panel_subcategory = models.CharField(max_length=25)
    panel_name = models.CharField(max_length=25)

class Gene(models.Model):
    """
    Model to store gene details
    """
    gene_id = models.AutoField(primary_key=True)
    # ensembl gene ID begining ENSG
    ensembl_gene_id = models.CharField(max_length=15)
    bedfile_request_id = models.ForeignKey('BedfileRequest', on_delete=models.CASCADE)

class Transcript(models.Model):
    """
    Model to store transcript details
    """
    transcript_id = models.AutoField(primary_key=True)
    # ensembl transcript ID begining ENST
    ensembl_transcript_id = models.CharField(max_length=15)
    # RefSeq transcript ID begining NM
    RefSeq_transcript_id = models.CharField(max_length=15)
    bedfile_request_id = models.ForeignKey('BedfileRequest', on_delete=models.CASCADE)
    gene_id = models.ForeignKey('Gene', on_delete=models.CASCADE)
    display_name = models.CharField(max_length=15)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    MANE_transcript = models.BooleanField()
    RefSeq_HGMD_transcript = models.BooleanField()
    clinvar_variant_coverage = models.FloatField()
    coding_transcript = models.BooleanField()
    full_ensembl_transcript_id = models.CharField(max_length=20)
    full_RefSeq_transcript_id = models.CharField(max_length=20)
    
class SelectedTranscript(models.Model):
    """
    Model to store transcript details
    """ 
    selected_transcript_id = models.AutoField(primary_key=True)   
    transcript_id = models.ForeignKey('Transcript', on_delete=models.CASCADE)
    transcript_padding = models.IntegerField()
    include_introns = models.BooleanField()
    exon_padding = models.IntegerField()
    include_five_prime_UTR = models.BooleanField()
    include_three_prime_UTR = models.BooleanField()
    five_prime_UTR_padding = models.IntegerField()
    three_prime_UTR_padding = models.IntegerField()