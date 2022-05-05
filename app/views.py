from django.shortcuts import render, redirect
from django.conf import settings
from django.template import RequestContext
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import make_aware

import os
import json
import requests
import datetime
import asyncio
import django_rq

from .mock_iot import send_iot_message
from .forms import CustomUserCreationForm, SubscriptionForm
from .models import NewsletterSubscription, CustomUser, PressReleaseSubmission
from .generate_pr import get_pr_prompt, generate_press_release
from .view_helpers import generate_context
from .auth_helpers import log_in, log_out, sign_up, activate, approval_check
from newsletter.settings import DEBUG

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
@user_passes_test(approval_check, login_url="/not-active/")
def app(request):
    if request.method == "GET":
        return render(request, 'app_landing_page.html', generate_context(request))

def prohibited(request):
    return HttpResponseForbidden("Wrong link, cowboy. Contact support if needed")

@login_required(login_url='/login/')
@user_passes_test(approval_check, login_url="/not-active/")
def submit_data_backend(request):
    data = json.loads(request.body.decode('UTF-8'))
    cow_status = data["status"]
    asyncio.run(send_iot_message(cow_status))
    return JsonResponse({})

@login_required(login_url='/login/')
@user_passes_test(approval_check, login_url="/not-active/")
def generate_pr(request):
    if request.method == "GET":
        submission_id = request.GET.get("id")
        try:
            submission = PressReleaseSubmission.objects.get(submission_id=submission_id)
        except ObjectDoesNotExist:
            response = response = {
                "id": submission_id,
                "status": "ERROR: Invalid ID"
            }
            return response
    
        if submission.is_complete():
            response = {
                "id": submission_id,
                "status": submission.submission_status,
                "generated_text": submission.generated_text,
                "num_credits": submission.user.num_credits
            }
        elif submission.is_error():
            response = {
                "id": submission_id,
                "status": submission.submission_status,
                "error_msg": submission.generated_text
            }
        else:
            response = {
                "id": submission_id,
                "status": submission.submission_status
            }
        print(response)
        return JsonResponse(response)

    elif request.method == "POST":
        # wat u doin here
        if request.user.num_credits == 0 or not request.user.admin_approved or not request.user.is_authenticated or not request.user.email_confirmed:
            response = {
                "id": 0,
                "status": "Error: Either user is not authenticated or has zero generation credits."
            }
            return JsonResponse(response)
        
        
        prompt, submission_attrs = get_pr_prompt(request)
        submission_attrs["user"] = request.user
        submission_attrs["submission_date"] = make_aware(datetime.datetime.now())
        submission = PressReleaseSubmission(**submission_attrs)
        submission.save()
        print(submission.submission_id)
        django_rq.enqueue(generate_press_release, prompt, submission.submission_id)

        response = {
            "id": submission.submission_id,
            "status": str(submission.submission_status)
        }
        print(response)
        return JsonResponse(response)

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
        
@login_required(login_url='/login/')
@user_passes_test(approval_check, login_url="/not-active/")
def submit_data(request):
    if request.method == "GET":
        return render(request, 'submit_data.html', generate_context(request, 
                                                    {"num_credits":request.user.num_credits,
                                                    "disabled":request.user.num_credits==0,
                                                    "email_confirmed":request.user.email_confirmed}))


@login_required(login_url='/login/')
@user_passes_test(approval_check, login_url="/not-active/")
def history(request):
    history = PressReleaseSubmission.objects.filter(user=request.user)
    return render(request, 'history.html', generate_context(request, 
                                                    {"num_credits":request.user.num_credits,
                                                    "disabled":request.user.num_credits==0,
                                                    "email_confirmed":request.user.email_confirmed,
                                                    "history":history}))


def not_active(request):
    if approval_check(request.user):
        return redirect('/app/press-release/')
        
    return render(request, "not-active.html", generate_context(request))

def privacy(request):
    return render(request, 'privacy-policy.html', generate_context(request))

def terms(request):
    return render(request, 'terms-conditions.html', generate_context(request))