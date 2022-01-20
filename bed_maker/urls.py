from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manual_import/', views.manual_import, name='manual_import'),
    path('view/', views.view, name='view'),
    path('edit/', include('edit_data.urls')),
    path('export/', include('export_bedfile.urls')),
]