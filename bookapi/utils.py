from django.core.mail import send_mail
from django.conf import settings


def send_email_to_client():
    subject = "Verification Email"
    message = "Verify your Email"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['shubhamnaugai27121@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
