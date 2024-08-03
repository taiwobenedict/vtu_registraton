from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, DomainForm, ChangePasswordForm, ProfileForm
from .models import License
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
import hashlib
import random
import string


def generate_activation_key():
    characters = string.hexdigits.lower()
    key = "".join(random.choice(characters) for _ in range(32))
    return key


def generate_secret_key(activation_key, domain_name):
    combined_string = activation_key + domain_name
    hash_object = hashlib.sha256(combined_string.encode())
    secret_key = hash_object.hexdigest()
    return secret_key


# Create your views here.
class LicenseView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = License
    template_name = "index.html"
    login_url = "/login/"
    ordering = "-created_at"


@login_required(login_url="/login/")
def generate_domain_key(request):

    license = {}

    if request.method == "POST":
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data["domain"]

            try:
                obj = License.objects.get(domain=domain)
            except License.DoesNotExist:
                obj = None

            if not obj:
                activation_key = generate_activation_key()
                secret_key = generate_secret_key(activation_key, domain_name=domain)

                license = License.objects.create(
                    domain=domain, activation_key=activation_key, secret_key=secret_key
                )
                messages.success(request, "Key successfully generated")
            else:
                messages.error(request, "Domain already exist!", "danger")

    form = DomainForm()
    return render(request, "generate_key.html", {"form": form, "license": license})

@login_required(login_url="/login/")
def domain_view(request, id):
    if request.method == "GET":
        action = request.GET.get("domain", "")
        license = License.objects.get(id=id)
        
        if action == "deactivate":
            license.is_active = False
        elif action == "activate":
            license.is_active = True
        elif action == "delete":
            license.delete()
            return HttpResponseRedirect("/")
            
        license.save()
            
        
        return render(request, "edit.html", {"license": license})


@api_view(["POST"])
def verify_domain_key(request):
    activation_key = request.data.get("activation_key", "")
    domain = request.data.get("domain", "")
    try:
        obj = License.objects.get(domain=domain, activation_key =activation_key)
    except License.DoesNotExist:
        obj = None
    if obj:  
        obj.key_sent = True
        obj.save()
        secret_key = obj.secret_key 
        
        return Response({"secret_key": secret_key}, status=200)
    else:
        return Response({'error': 'Key not registered'},status=400)


def login_view(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/")
            else:
                messages.error(request, "Username or Password Incorrect!")
                return render(request, "login.html", {"form": form})

    else:
        # Return an 'invalid login' error message.
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    
@login_required(login_url="/login/")   
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def profile(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, profile_form.errors)
        return redirect('profile')

    else:
        profile_form = ProfileForm(instance=request.user)
        

    return render(request, "profile.html", {"profile": profile_form})

@login_required(login_url="/login/")
def change_password(request):
    if request.method == "POST":
        password_form = ChangePasswordForm(data=request.POST)
        
        if password_form.is_valid():
            new_password = password_form.cleaned_data.get('new_password')
            confirm_password = password_form.cleaned_data.get('confirm_password')
            current_password = password_form.cleaned_data.get("current_password")
            
            if request.user.check_password(current_password):
                if  new_password != confirm_password:
                    messages.error(request,"Passwords did'nt match!")
                else:
                    request.user.set_password(new_password)
                    login(request, request.user)
                    messages.success(request, "You've successfully changed your password!")
                    request.user.save()
            else:
                messages.error(request,'Current password not correct!')
                    
    password_form = ChangePasswordForm()
    return render(request, 'change_password.html', {"form": password_form})

