from django import forms
from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Имя пользователя')
    email = forms.EmailField(required=True, label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль')
    status = forms.ChoiceField(choices=[('user', 'Пользователь'), ('admin', 'Администратор')], required=True, label='Статус')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Имя пользователя может содержать только буквы, цифры и подчеркивания.')
        if len(username) < 3:
            raise ValidationError('Имя пользователя должно содержать минимум 3 символа.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise ValidationError('Введите действительный адрес электронной почты.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')
        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            raise ValidationError('Пароль должен содержать как буквы, так и цифры.')
        return password

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Пароль')
    remember_me = forms.BooleanField(required=False, label='Запомнить пароль')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Имя пользователя может содержать только буквы, цифры и подчеркивания.')
        return username