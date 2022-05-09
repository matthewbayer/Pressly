from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .forms import CustomUserCreationForm, SubscriptionForm
from .view_helpers import generate_context
from newsletter.settings import ADMIN_EMAIL as admin_email
from newsletter.settings import EMAIL_HOST_USER as email_host_user
import six

# Views
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
            #send_confirmation_email(request, email, user)
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




class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

def send_confirmation_email(request, to_email, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('email_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
    send_mail(mail_subject, message, email_host_user, [to_email])

    mail_subject = "New User Signup"
    message = user.email
    send_mail(mail_subject, message, email_host_user, [admin_email])


def approval_check(user):
    return user.is_approved()