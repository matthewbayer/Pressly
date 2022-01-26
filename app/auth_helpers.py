from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from newsletter.settings import ADMIN_EMAIL as admin_email
from newsletter.settings import EMAIL_HOST_USER as email_host_user
import six


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