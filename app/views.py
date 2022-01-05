from django.shortcuts import render
from django.conf import settings
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

import os

from .forms import CustomUserCreationForm

def render_to_json(request, data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
        mimetype=request.is_ajax() and "application/json" or "text/html"
    )


def index(request):
    return render(request, 'index.html')

def app(request):
    if not request.user.is_authenticated:
        return render(request, 'log-in.html')
    else:
        return render(request, 'app.html')

def log_in(request):
    if request.method == "GET":
        return render(request, 'log-in.html')
    elif request.method == "POST":
        username = request.POST.get("lemail")
        raw_password = request.POST.get("lpassword")
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/app/')
        else:
            error = "Invalid credentials. Try again."
            return render(request, 'log-in.html', {'error': error})


def sign_up(request):
    form = CustomUserCreationForm()
    if request.method == "GET":
        return render(request, 'sign-up.html', {'form': form})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'sign-up.html', {'form': form})
            
            #return form



def privacy(request):
    return render(request, 'privacy-policy.html')

def terms(request):
    return render(request, 'terms-conditions.html')