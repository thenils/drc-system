from django.urls import path

from .views import home, RegisterView, OTPView, LogoutView, LoginView

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('otp-verify/', OTPView.as_view(), name='otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout')
]
