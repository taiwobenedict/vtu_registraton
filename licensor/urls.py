from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", views.login_view, name= "login"),
    path("", views.LicenseView.as_view(), name='home'),
    path("domain/<str:id>/", views.domain_view, name='domain'),
    path("generate_domain_key/", views.generate_domain_key, name= "generate_domain_key"),
    path('verify_domain_key/', views.verify_domain_key, name='verify_domain_key'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
]
