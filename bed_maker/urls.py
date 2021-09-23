from django.urls import path, include
from django.conf.urls import url

from . import views

#app_name = 'bed_maker'
urlpatterns = [
    path('', views.home, name='home'),
    
    path('manual_import/', views.manual_import, name='manual_import'),
    path('view/', views.view, name='view'),
    
   
    
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('signup/', views.signup, name='signup'),
  
    path("password_reset/", views.password_reset_request, name="password_reset")

    
    
]