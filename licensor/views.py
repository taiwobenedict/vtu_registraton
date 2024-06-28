from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, DomainForm
from .models import License
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView


# Create your views here.
class LicenseView(ListView):
    paginate_by = 10
    model = License
    template_name = "index.html"

@login_required(login_url="/login/")
def generate_domain_key(request):
    
    license = {}
    
    if request.method == "POST":
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data['domain']
            
            # Check if domain or key already exist
            print(domain)
            try:
                obj = License.objects.get(domain = domain)
            except License.DoesNotExist:
                obj = None
            
            if not obj:
                license = License.objects.create(domain=domain)
                messages.success(request, "Key successfully generated")
            else:
                messages.error(request, "Domain already exist!","danger")
                
    form = DomainForm()
    return render(request, "generate_key.html", {"form": form, "license": license})


def domain_view(request,id):
    if request.method == "GET":
        license = License.objects.get(id = id)
        return render(request,"edit.html", {"license": license} )
        
 

@api_view(['POST'])
def verify_domain_key(request):
    pass
    
    
def login_view(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    
    if request.method == "POST":
        
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Username or Password Incorrect!')
                return render(request, "login.html", {"form": form})
            
        
    else:
        # Return an 'invalid login' error message.
        form = LoginForm()
        return render(request, "login.html", {"form": form})
            
