from django.contrib import admin

# Register your models here.
from .models import User, SessionOTP

admin.site.register(User)
admin.site.register(SessionOTP)