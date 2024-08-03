from  django import forms
from .models import License
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget= forms.TextInput(attrs= {"class":"form-control", "placeholder": "Username"}))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "Password"}))
    
    
class DomainForm(forms.Form):
    domain = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Domain"}))
    
    
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "Current Password"}))
    new_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "New Password"}))
    confirm_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "Confirm Password"}))
   
class ProfileForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control profile'}),
            'email': forms.EmailInput(attrs={'class': 'form-control profile'}),
        }