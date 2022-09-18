from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from user.decorators import logout_required
from user.form import UserCreateForm
from utils.modules import send_otp, clean_phone
from .models import SessionOTP, User
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
            otp_session = send_otp(user, 0)
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
        print(session_id, 'this is session')
        session = SessionOTP.objects.get(pk=session_id)
        print(session)
        if session.otp == int(otp):
            user = session.user
            if session.action == 0 or session.action == 2:
                user.is_active = True
                user.save()
            login(request, user)
            return redirect('/')

        return render(request, self.template_name, {'error': 'OTP did not match'})


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
                session_otp = send_otp(user, 1)
            else:
                session_otp = send_otp(user, 2)
            request.session['otp_session'] = session_otp
            return redirect('/otp-verify')
        except:
            return render(request, self.template_name, {'error': 'No user Found please Sign Up'})
