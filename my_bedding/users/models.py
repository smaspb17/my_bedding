from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(
        verbose_name='Телефон',
        unique=True,
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=250,
        verbose_name='Адрес',
        blank=True,
        null=True,
    )

    # class Meta:
    #     verbose_name = 'Пользователь'
    #     verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Профиль пользователя',
    )
    photo = models.ImageField(
        upload_to='media/users/',
        verbose_name='Фото',
        null=True,
        blank=True,
    )
    telegram_id = models.CharField(
        max_length=30, verbose_name='Telegram-ID', unique=True, null=True,
        blank=True, )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


