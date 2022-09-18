import random

from user.models import User, SessionOTP


def send_otp(request, user: User, action: int):
    otp = random.randint(100000, 999999)
    print(f'Your verification OTP is {otp}')
    request.session['otpSentCount'] = request.session.get('otpSentCount') + 1
    otp = SessionOTP.objects.create(user=user, action=action, otp=otp)
    return otp.id


def clean_phone(value):
    return value.replace('-', '').replace('+', '')