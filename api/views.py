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

class GeneList(generics.ListCreateAPIView):
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

