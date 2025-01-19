from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from easy_thumbnails.fields import ThumbnailerImageField

from .managers import CustomUserManager
from .validators import (
    validate_russian_phone,
    validate_first_name,
    validate_last_name,
    validate_telegram_id
)


class User(AbstractUser):
    first_name = models.CharField(
        max_length=100,
        blank=True,  # Позволяет оставлять поле пустым в формах
        null=True,  # Позволяет сохранять NULL в базе данных
        verbose_name='Имя',
        validators=[validate_first_name]
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,  # Позволяет оставлять поле пустым в формах
        null=True,  # Позволяет сохранять NULL в базе данных
        verbose_name='Фамилия',
        validators=[validate_last_name]
    )
    # Обязательно уникальный email, так как он используется для аутентификации
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False
    )
    phone_number = models.CharField(
        verbose_name='Телефон',
        unique=True,
        blank=True,
        null=True,
        max_length=12,  # Для номеров типа +7XXXXXXXXXX
        validators=[validate_russian_phone],
    )
    address = models.CharField(
        max_length=250,
        verbose_name='Адрес',
        blank=True,
        null=True,
    )
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # Присваиваем кастомный менеджер

    # отображать в админке по email
    def __str__(self):
        return f'id {self.id}'

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
    photo = ThumbnailerImageField(
        upload_to='media/users/',
        verbose_name='Фото',
        null=True,
        blank=True,
    )
    telegram_id = models.CharField(
        max_length=30,
        verbose_name='Telegram-ID',
        unique=True,
        null=True,
        blank=True,
        validators=[validate_telegram_id]
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


