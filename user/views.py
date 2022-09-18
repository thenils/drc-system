from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from user.decorators import logout_required
from user.form import UserCreateForm
from utils.modules import send_otp, clean_phone
from .models import SessionOTP, User, Email
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'user/home.html')


# Create your views here.
class RegisterView(TemplateView):
    """
        Registration View for template
    """
    template_name = 'user/signup.html'

    def get(self, request):
        return render(request, self.template_name, {'form': UserCreateForm})

    @method_decorator(logout_required)
    def post(self, request, **kwargs):
        print('this is working')
        data = request.POST
        form = UserCreateForm(data)
        if form.is_valid():
            user = form.create(form.data)
            otp_session = send_otp(request, user, 0)
            request.session['otp_session'] = otp_session

            return redirect('/otp-verify')
        return render(request, 'user/signup.html', {'form': form})


class OTPView(TemplateView):
    """
        Registration View for template
    """
    template_name = 'user/otp.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        data = request.POST
        otp = data.get('otp', None)
        session_id = request.session.get('otp_session')
        session = SessionOTP.objects.get(pk=session_id)
        user = session.user
        if session.otp == int(otp):
            if session.action == 0 or session.action == 2:
                user.is_active = True
                user.save()
            del request.session['otp_session']
            del request.session['otpSentCount']
            login(request, user)
            return redirect('/')

        return render(request, self.template_name, {'error': 'OTP did not match'})


def resend_otp(request):
    session_id = request.session.get('otp_session')
    session = SessionOTP.objects.get(pk=session_id)
    sent_count = request.session.get('otpSentCount')
    if sent_count > 3:
        if (sent_count % 3) + 1 == 1 and session.action == 1 and session.createdAt + timedelta(
                minutes=5) > timezone.now():
            return render(request, 'user/otp.html', {'error': 'you limit exhausted wait for 5 min to resend otp'})
    send_otp(request, session.user, 1)
    return render(request, 'user/otp.html')


def LogoutView(request):
    logout(request)
    return redirect('/')


class LoginView(TemplateView):
    template_name = 'user/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        data = request.POST
        phone = clean_phone(data.get('phone_number'))
        try:
            user = User.objects.get(phone=phone)
            if user.is_active:
                session_otp = send_otp(request, user, 1)
            else:
                session_otp = send_otp(request, user, 2)
            request.session['otp_session'] = session_otp
            return redirect('/otp-verify')
        except:
            return render(request, self.template_name, {'error': 'No user Found please Sign Up'})


class ProfileView(TemplateView):
    template_name = 'user/profile.html'

    def get(self, request):
        user = request.user
        emails = Email.objects.filter(user=user)
        return render(request, self.template_name, {'user': user, 'emails': emails})

    def post(self, request):
        email = request.POST['email']
        Email.objects.create(email=email, user=request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def set_email_primary(request, user_id: int, email_id: int):
    emails = Email.objects.filter(user_id=user_id)
    for email in emails:
        if email.isPrimary and email.id != email_id:
            email.isPrimary = False
            email.save()
        if email.id == email_id:
            email.isPrimary = True
            email.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
