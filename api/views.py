from django.shortcuts import render
from rest_framework import generics, fields
from bed_maker.models import *
from .serializers import BedfileRequestSerializer, GeneSerializer, TranscriptSerializer
import django_filters.rest_framework

class BedfileRequestList(generics.ListCreateAPIView):
    queryset = BedfileRequest.objects.all()
    serializer_class = BedfileRequestSerializer

class BedfileRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BedfileRequest.objects.all()
    serializer_class = BedfileRequestSerializer

class BedfileRequestList(generics.ListCreateAPIView):
    '''
    Return list of bedfile requests
    http://127.0.0.1:8000/api/v1/genes/?format=json&bedfile_request_id=1
    '''
    queryset = BedfileRequest.objects.all()
    serializer_class = BedfileRequestSerializer
class GeneList(generics.ListCreateAPIView):
    '''
    Return list of genes + filter on BedfileRequestId
    http://127.0.0.1:8000/api/v1/genes/?format=json&bedfile_request_id=1
    '''
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
    filter_fields = (
        'bedfile_request_id',
    )
   
class GeneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer

class TranscriptList(generics.ListCreateAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer

class TranscriptDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer

