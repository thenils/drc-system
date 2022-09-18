import random
from datetime import timedelta

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as gl
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, phone, username, password=None, **extra_fields):
        """Create New User"""
        user = self.model(phone=phone, **extra_fields)
        user.username = f'{username}-{random.randint(1, 200000)}'
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, phone, password):
        """Create New Super User"""
        user = self.create_user(phone, 'staff', password)
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):
        """Create New Super User"""
        user = self.create_user(phone, 'super', password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=35, unique=True)
    phone = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    profile = models.FileField(upload_to='profile/')
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    objects = UserManager()

    def __str__(self):
        return self.username


class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='emails')
    email = models.EmailField(gl('email address'), unique=True)
    isPrimary = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Email Addresses'

    def __str__(self):
        return f'{self.email}, {self.isPrimary}'


class SessionOTP(models.Model):
    ACTION_CHOISE = (
        (0, 'SIGN UP'),
        (1, 'LOGIN'),
        (2, 'ACTIVATE')
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    otp = models.IntegerField()
    action = models.IntegerField(default=1, choices=ACTION_CHOISE)
    createdAt = models.DateTimeField(auto_now=True)
    expireAt = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))

    def __str__(self):
        return f'{self.user.username}, OTP- {self.otp}'
