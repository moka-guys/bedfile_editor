from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manual_enter_region/', views.manual_enter_region, name='manual_enter_region'),
    path('view/', views.view, name='view'),
]