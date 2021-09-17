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