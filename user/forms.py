from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from user.models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'last_name', 'middle_name', 'address')
        labels = {
            'phone': 'Телефон',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'address': 'Адрес',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(label='Номер телефона', widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
