import random

from user.models import User, SessionOTP


def send_otp(user: User, action: int):
    otp = random.randint(100000, 999999)
    otp = SessionOTP.objects.create(user=user, action=action, otp=otp)
    return otp.id


def clean_phone(value):
    return value.replace('-', '').replace('+', '')