from django.urls import path
from .views import SelectBedfile

urlpatterns = [
    path('', SelectBedfile, name='edit'),
]