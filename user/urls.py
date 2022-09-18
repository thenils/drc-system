from django.urls import path

from .views import home, RegisterView, OTPView, LogoutView, LoginView, ProfileView, set_email_primary, resend_otp

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('otp-verify/', OTPView.as_view(), name='otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('make_primary_mail/<int:user_id>/<int:email_id>/', set_email_primary, name='set_primary'),
    path('resend_otp/', resend_otp, name='resend-otp'),
]
