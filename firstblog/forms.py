from django import forms
from .models import HousingData
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    status = forms.ChoiceField(choices=[('regular', 'Обычный'), ('admin', 'Администратор')])

