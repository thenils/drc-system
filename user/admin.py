from django.contrib import admin

# Register your models here.
from .models import User, SessionOTP, Email

admin.site.register(User)
admin.site.register(SessionOTP)
admin.site.register(Email)
