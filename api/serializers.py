from rest_framework import serializers
from bed_maker.models import BedfileRequest, Gene, Transcript
from django_restql.mixins import DynamicFieldsMixin 

class BedfileRequestSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    
    class Meta:
        fields = ('bedfile_request_id', 'pan_number', 'date_requested', 'requested_by', 'request_status', 'request_transcript_padding', 'request_introns', 'request_exon_padding', 'request_five_prime_UTR', 'request_three_prime_UTR', 'request_five_prime_UTR_padding', 'request_three_prime_UTR_padding', 'panel_category', 'panel_subcategory', 'panel_name',)
        model = BedfileRequest

class BedfileRequestSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    
    class Meta:
        fields = ('bedfile_request_id', 'pan_number', 'date_requested', 'requested_by', 'request_status', 'request_transcript_padding', 'request_introns', 'request_exon_padding', 'request_five_prime_UTR', 'request_three_prime_UTR', 'request_five_prime_UTR_padding', 'request_three_prime_UTR_padding', 'panel_category', 'panel_subcategory', 'panel_name',)
        model = BedfileRequest

class TranscriptSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('transcript_id','ensembl_id',
    'ensembl_transcript_version', 'RefSeq_transcript_id',
    'RefSeq_transcript_version', 'bedfile_request_id', 'gene_id', 'display_name', 'chromosome', 'start', 'end', 'MANE_transcript', 'RefSeq_HGMD_transcript', 'biotype', 'coverage', 'clinvar_coverage', 'clinvar_variants', 'clinvar_details', 'recommended_transcript', 'selected_transcript', 'transcript_padding', 'include_introns', 'include_exon_padding', 'include_five_prime_UTR', 'include_three_prime_UTR','five_prime_UTR_padding', 'three_prime_UTR_padding')
        model = Transcript


class GeneSerializer(serializers.ModelSerializer):
    gene_transcripts = TranscriptSerializer(read_only=True, many=True)
    class Meta:
        fields = ('gene_id', 'ensembl_id', 'bedfile_request_id', 'gene_transcripts',)
        model = Gene
