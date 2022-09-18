import random

from django import forms
from user.models import Email, User
from utils.modules import clean_phone, welcome_mail


class UserCreateForm(forms.Form):
    email = forms.EmailField(required=False, max_length=45)
    phone = forms.CharField(max_length=16, required=True)
    first_name = forms.CharField(max_length=25, required=True)
    last_name = forms.CharField(max_length=25, required=True)
    username = forms.CharField(max_length=35)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['email', 'phone', 'first_name', 'last_name', 'username', 'password', 'password2']

    def clean(self):
        data = super().clean()
        email = data.get('email', None)
        if email and Email.objects.filter(email=email).exists():
            raise forms.ValidationError({'email': ['this email is already exists!']})

        phone = clean_phone(data['phone'])
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError({'phone': ['This number already use in with another account']})

        if 'username' not in data:
            username_exists = True
            while username_exists:
                username = f'User{random.randint(1, 2000)}'
                users = User.objects.filter(username=username)
                if users.exists():
                    username_exists = True
                else:
                    username_exists = False
                    data.update({'username': username})
        else:
            username = data['username']
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError({'username': ['username is already exists!']})

        if data['password'] != data['password2']:
            raise forms.ValidationError({'password2': ['password is not matching!']})

        return data

    def create(self, data):

        user = User.objects.create(phone=data['phone'], username=data['username'],
                                   first_name=data['first_name'],
                                   last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        if 'email' in data:
            Email.objects.create(user=user, email=data['email'], isPrimary=True)
            welcome_mail(data['email'], user)

        return user


