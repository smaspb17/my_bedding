import re

from phonenumber_field.validators import validate_international_phonenumber
from django.core.exceptions import ValidationError


from django.core.exceptions import ValidationError
from phonenumbers import parse, is_valid_number, NumberParseException


def validate_russian_phone(value):
    if not re.match(r'^(?:\+7|8)', value):
        raise ValidationError('номер телефона должен начинаться с +7 или 8')
    elif not re.match(r'^(?:\+7|8)\d{10}$', value):
        raise ValidationError('некорректная длина телефона')


def validate_first_name(value):
    if not value.isalpha():
        raise ValidationError('имя должно содержать только буквы')


def validate_last_name(value):
    if not value.isalpha():
        raise ValidationError('фамилия должна содержать только буквы')


def validate_user_address(value):
    if not re.match(r'\d{6}', value):
        raise ValidationError('адрес должен начинаться с индекса из 6 цифр')


def validate_pickup_point_address(value):
    if value is None or value in ['Адрес не найден', 'Индекс не указан']:
        raise ValidationError('адрес доставки не определен')
    elif not re.match(r'\d{6}', value):
        raise ValidationError('адрес должен начинаться с индекса из 6 цифр')
