from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    path("login/", views.login_view, name= "login"),
    path("", views.LicenseView.as_view(), name='home'),
    path("domain/<str:id>/", views.domain_view, name='domain'),
    path("generate_domain_key/", views.generate_domain_key, name= "generate_domain_key"),
    path('verify_domain_key/', views.verify_domain_key, name='verify_domain_key'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    
    path('password-reset/', PasswordResetView.as_view(),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]
