import re
import logging

from django import forms
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.core import exceptions
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .models import Profile

User = get_user_model()


class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
    )
    captcha = forms.CharField(required=False)
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'password2', 'captcha']
        # fields = ['email', 'password', 'password2']

    def clean_password(self):
        password = self.cleaned_data.get('password')  # Используем get()
        email = self.cleaned_data.get('email')  # Используем get()
        #
        # if password is None:
        #     raise forms.ValidationError("Пароль не был предоставлен")

        # Проверка длины пароля
        if not 7 <= len(password) <= 30:
            raise forms.ValidationError('Длина пароля от 7 до 30 символов')

        # Проверка сложности пароля
        if any([not re.search(r'\d', password),
                not re.search(r'[A-Z]|[a-z]|[А-Я]|[а-я]', password),
               # not re.search(r'[!@#$%^&*(),.?":{}|<>]', password),
                ]):
            raise forms.ValidationError('Пароль должен содержать буквы и цифры')

        # Проверка равенства email и пароля
        if email == password:
            raise forms.ValidationError('Пароль не должен совпадать с Email')

        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2:
            if password != password2:
                raise forms.ValidationError('Пароли не совпадают')
        return password2
    #
    # def clean_captcha(self):
    #     print('Вызов clean_captcha')
    #     captcha = self.cleaned_data.get('captcha')
    #     if not captcha:
    #         raise exceptions.ValidationError('Captcha не пройдена')
    #     return captcha


class LoginUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    # def clean_password(self):
    #     email = self.cleaned_data['email']
    #     password = self.cleaned_data['password']
    #     if not User.objects.get(email=email) or


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
        self.fields['email'].label = 'Введите email'


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', ]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telegram_id']


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False  # Убираем обязательность
            field.widget.attrs.pop('required', None)  # Убираем HTML-атрибут required
            field.widget.attrs.pop('autofocus', None)  # Убираем HTML-атрибут required

    def clean(self):
        cleaned_data = super().clean()

        # Проверяем, если одно из полей заполнено, все остальные должны быть заполнены
        fields = ['old_password', 'new_password1', 'new_password2']
        if any(cleaned_data.get(field) for field in fields):
            if not all(cleaned_data.get(field) for field in fields):
                raise forms.ValidationError("Для смены пароля заполните все поля.")

        return cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        # Если поле заполнено, проверяем корректность
        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError("Ваш старый пароль указан неверно.")

        return old_password

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        email = self.user.email

        # Проверка длины пароля
        if new_password1 and not 7 <= len(new_password1) <= 30:
            raise forms.ValidationError('Длина пароля должна быть от 7 до 30 символов.')

        # Проверка сложности пароля
        if new_password1 and not re.search(r'\d', new_password1):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну цифру.')
        if new_password1 and not re.search(r'[A-Za-zА-Яа-я]', new_password1):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну букву.')

        # Проверка, чтобы пароль не совпадал с email
        if new_password1 and email == new_password1:
            raise forms.ValidationError('Пароль не должен совпадать с Email.')

        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        # Проверка на совпадение паролей
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('Пароли не совпадают.')

        return new_password2

