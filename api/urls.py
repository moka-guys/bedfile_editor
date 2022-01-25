from django.urls import path
from .views import BedfileRequestDetail, BedfileRequestList, GeneDetail, GeneList, TranscriptList, TranscriptDetail

urlpatterns = [
    path('<int:pk>/', BedfileRequestDetail.as_view()),
    path('bedfilerequests/', BedfileRequestList.as_view()),
    path('bedfilerequests/<int:pk>/', BedfileRequestDetail.as_view()),
    path('', BedfileRequestList.as_view()),
    path('genes/<int:pk>/', GeneDetail.as_view()),
    path('genes/', GeneList.as_view()),
    path('transcripts/<int:pk>/', TranscriptDetail.as_view()),
    path('transcripts/', TranscriptList.as_view()),
]