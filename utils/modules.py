import random

from django.conf import settings
from django.core.mail import send_mail

from user.models import User, SessionOTP


def send_otp(request, user: User, action: int):
    otp = random.randint(100000, 999999)
    print(f'Your verification OTP is {otp}')
    request.session['otpSentCount'] = request.session.get('otpSentCount') if request.session.get(
        'otpSentCount') else 0 + 1
    otp = SessionOTP.objects.create(user=user, action=action, otp=otp)
    return otp.id


def clean_phone(value):
    return value.replace('-', '').replace('+', '')


def welcome_mail(email, user: User):
    subject = 'welcome to DRC system'
    message = f'Hi {user.username}, we are very happy to have you on board! regards, Nilesh Nandaniya'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
