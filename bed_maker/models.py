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
    ensembl_transcript_version = models.CharField(max_length=3, default="")
    # RefSeq transcript ID begining NM
    RefSeq_transcript_id = models.CharField(max_length=15)
    RefSeq_transcript_version = models.CharField(max_length=3, default="")
    bedfile_request_id = models.ForeignKey('BedfileRequest', on_delete=models.CASCADE)
    gene_id = models.ForeignKey('Gene', on_delete=models.CASCADE)
    display_name = models.CharField(max_length=15)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    MANE_transcript = models.BooleanField()
    RefSeq_HGMD_transcript = models.BooleanField(default=False)
    clinvar_variant_coverage = models.FloatField(default=0)
    biotype = models.CharField(max_length=21, default="")
    
class SelectedTranscript(models.Model):
    """
    Model to store transcript details
    """ 
    selected_transcript_id = models.AutoField(primary_key=True)   
    transcript_id = models.ForeignKey('Transcript', on_delete=models.CASCADE)
    transcript_padding = models.IntegerField(default=0)
    include_introns = models.BooleanField(default=False)
    exon_padding = models.IntegerField(default=0)
    include_five_prime_UTR = models.BooleanField(default=False)
    include_three_prime_UTR = models.BooleanField(default=False)
    five_prime_UTR_padding = models.IntegerField(default=False)
    three_prime_UTR_padding = models.IntegerField(default=False)