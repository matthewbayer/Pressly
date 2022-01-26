from django.shortcuts import render
from django.conf import settings
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test

import os
import requests
import datetime

from .forms import CustomUserCreationForm, SubscriptionForm
from .models import NewsletterSubscription, CustomUser, PressReleaseSubmission
from .generate_pr import get_pr_prompt, generate_from_prompt
from .auth_helpers import send_confirmation_email, account_activation_token, approval_check

from rq import Queue
from .worker import conn

q = Queue(connection=conn)

def generate_context(request, extra=None):
    logged_in = request.user.is_authenticated
    context = {"logged_in": logged_in}
    if extra:
        context = {**context, **extra}
    return context

def handler404(request, *args, **argv):
    response = render('404.html', generate_context(request))
    response.status_code = 404
    return response

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

def prohibited(request):
    return HttpResponseForbidden("Wrong link, cowboy. Contact support if needed")

@login_required(login_url='/login/')
@user_passes_test(approval_check, login_url="/not-active/")
def press_release(request):
    if request.method == "GET":
        #if not request.user.is_authenticated:
        #    return render(request, 'log-in.html', generate_context(request))
        #else:
        return render(request, 'app.html', generate_context(request, 
                                                            {"num_credits":request.user.num_credits,
                                                            "disabled":request.user.num_credits==0,
                                                            "email_confirmed":request.user.email_confirmed}))
    elif request.method == "POST":
        # wat u doin here
        if request.user.num_credits == 0:
            return HttpResponseRedirect('/')
        
        try:
            prompt, submission_attrs = get_pr_prompt(request)
            #print(prompt)
            content = q.enqueue(generate_from_prompt(prompt))
            #content = {"generated_text": "test conent\n\testing\nasdasfas\n\nabc123"}
            content["num_credits"] = request.user.num_credits - 1
            user = CustomUser.objects.filter(email=request.user.email)
            user.update(num_credits=request.user.num_credits-1)
        except requests.exceptions.RequestException as e:
            content = {"generated_text": "An error occurred generating your content. Please try again."}
            content["num_credits"] = request.user.num_credits
            print(e)
        except ValueError:
            content = {"generated_text": "Error reading in your submission - ensure your date is properly formatted."}
            content["num_credits"] = request.user.num_credits

        content["generated_text"] = content["generated_text"].replace("\n", "\n")
        
        print(content)

        # record the submission in db
        submission_attrs["user"] = request.user
        submission_attrs["generated_text"] = content["generated_text"]
        submission_attrs["submission_date"] = datetime.datetime.now()
        submission = PressReleaseSubmission(**submission_attrs)
        submission.save()

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
    #return render(request, 'log-out.html', generate_context(request))
    return HttpResponseRedirect('/app/')

def sign_up(request):
    form = CustomUserCreationForm()
    if request.method == "GET":
        return render(request, 'sign-up.html', generate_context(request, {'form': form}))
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            send_confirmation_email(request, email, user)
            login(request, user)
            return HttpResponseRedirect('/app/')
        else:
            return render(request, 'sign-up.html', generate_context(request, {'form': form}))

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Your account setup is now complete.')
    else:
        return HttpResponse('Activation link is invalid!')

def not_active(request):
    return render(request, "not-active.html", generate_context(request))

def privacy(request):
    return render(request, 'privacy-policy.html', generate_context(request))

def terms(request):
    return render(request, 'terms-conditions.html', generate_context(request))