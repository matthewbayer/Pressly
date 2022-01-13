from django.shortcuts import render
from django.conf import settings
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import os
import requests

from .forms import CustomUserCreationForm, SubscriptionForm
from .models import NewsletterSubscription, CustomUser
from .generate_pr import get_pr_prompt, generate_from_prompt

def generate_context(request, extra=None):
    logged_in = request.user.is_authenticated
    context = {"logged_in": logged_in}
    if extra:
        context = {**context, **extra}
    return context   

def index(request):
    if request.method == "GET":
        return render(request, 'index.html', generate_context(request))
    elif request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'index.html', generate_context(request))
        else:
            return render(request, 'index.html', generate_context(request, {'form': form}))
    
@login_required(login_url='/login/')
def app(request):
    if request.method == "GET":
        return render(request, 'app_landing_page.html', generate_context(request))

@login_required(login_url='/login/')
def press_release(request):
    if request.method == "GET":
        #if not request.user.is_authenticated:
        #    return render(request, 'log-in.html', generate_context(request))
        #else:
        return render(request, 'app.html', generate_context(request, {"credits":request.user.num_credits, "disabled":request.user.num_credits==0}))
    elif request.method == "POST":
        #if not request.user.is_authenticated:
        #    return render(request, 'log-in.html', generate_context(request))
        #else:
        # wat u doin here
        if request.user.num_credits == 0:
            return HttpResponseRedirect('/')

        prompt = get_pr_prompt(request)
        try:
            #content = generate_from_prompt(prompt)
            content = {"generated_text": "test conent\n\testing\nasdasfas\n\nabc123"}
            user = CustomUser.objects.filter(email=request.user.email)
            user.update(num_credits=request.user.num_credits-1)
        except requests.exceptions.RequestException as e:
            content = {"generated_text": "An error occurred generating your content. Please try again."}
            print(e)

        content["generated_text"] = content["generated_text"].replace("\n", "\n")
        content["num_credits"] = request.user.num_credits

        return JsonResponse(content)
            
def log_in(request):
    if request.method == "GET":
        return render(request, 'log-in.html', generate_context(request))
    elif request.method == "POST":
        username = request.POST.get("lemail")
        raw_password = request.POST.get("lpassword")
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/app/')
        else:
            error = "Invalid credentials. Try again."
            return render(request, 'log-in.html', generate_context(request, {'error': error}))

def log_out(request):
    logout(request)
    return render(request, 'log-out.html', generate_context(request))

def sign_up(request):
    form = CustomUserCreationForm()
    if request.method == "GET":
        return render(request, 'sign-up.html', generate_context(request, {'form': form}))
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/app/')
        else:
            return render(request, 'sign-up.html', generate_context(request, {'form': form}))
            
            #return form



def privacy(request):
    return render(request, 'privacy-policy.html', generate_context(request))

def terms(request):
    return render(request, 'terms-conditions.html', generate_context(request))