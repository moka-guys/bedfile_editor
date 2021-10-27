"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from Profiles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bed_maker.urls')),
    #path('', include('Profiles.urls')),
    path('accounts', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    #path('', include(('bed_maker.urls', 'password_reset'), namespace='password_reset')),

    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Profiles/password_reset_table.html'), name='password_reset'),
    path('password_reset/', views.password_reset_request, name='password_reset'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='Profiles/password_change.html'), 
        name='password_change'),


    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='Profiles/password_change_finished.html'), 
        name='password_change_done'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Profiles/password_reset_finished.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Profiles/password_reset_confirmed.html'), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Profiles/password_reset_completed.html'),
     name='password_reset_complete'),

    path('login/not_activated/', auth_views.PasswordResetCompleteView.as_view(template_name='Profiles/account_not_activated.html'),
     name='account_not_activated'),
    
    path('login/wrong_password/', auth_views.PasswordResetCompleteView.as_view(template_name='Profiles/wrong_password_entered.html'),
     name='wrong_password_entered'),    
    path('password_reset/email_not_found/', auth_views.PasswordResetCompleteView.as_view(template_name='Profiles/email_not_recognised.html'),
     name='email_not_recognised'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]
