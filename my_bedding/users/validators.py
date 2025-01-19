import re
from django.core.exceptions import ValidationError


def validate_russian_phone(value):
    if not re.match(r'^(?:\+7|8)', value):
        raise ValidationError('Номер телефона должен начинаться с +7 или 8')
    elif not re.match(r'^(?:\+7|8)\d{10}$', value):
        raise ValidationError('Некорректная длина телефона')


def validate_first_name(value):
    if not value.isalpha():
        raise ValidationError('Имя должно содержать только буквы')


def validate_last_name(value):
    if not value.isalpha():
        raise ValidationError('Фамилия должна содержать только буквы')


def validate_telegram_id(value):
    # Регулярное выражение для проверки telegram_id: начинается с @, затем буквы, цифры и подчеркивания
    telegram_pattern = r"^@[A-Za-z0-9_]{5,32}$"  # начинается с @, затем буквы, цифры и подчеркивания, длина от 5 до 32 символов
    if not re.match(telegram_pattern, value):
        raise ValidationError(
            "Должен начинаться с @, содержать буквы, цифры и _, длина от 5 до 32"
        )