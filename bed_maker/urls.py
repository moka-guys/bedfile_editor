from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manual_import/', views.manual_import, name='manual_import'),
    path('view/', views.view, name='view'),
]