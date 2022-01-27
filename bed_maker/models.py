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
    MANE_transcript = models.BooleanField()
    RefSeq_HGMD_transcript = models.BooleanField(default=False)
    biotype = models.CharField(max_length=50, default="")
    coverage = models.CharField(max_length=20)
    clinvar_coverage = models.CharField(max_length=10)
    clinvar_variants = models.CharField(max_length=50)
    clinvar_details = models.CharField(max_length=50)
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