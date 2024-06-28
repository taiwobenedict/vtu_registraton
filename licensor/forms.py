from  django import forms
from .models import License

class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        fields = "__all__"

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget= forms.TextInput(attrs= {"class":"form-control", "placeholder": "Username"}))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "Password"}))
    
    
class DomainForm(forms.Form):
    domain = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Domain"}))