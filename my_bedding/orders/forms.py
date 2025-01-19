from django import forms

from phonenumbers import parse, format_number, PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException, is_valid_number

from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'user_address',
                  'pickup_point_address',]

    # def clean_phone(self):
    #     phone = self.cleaned_data['phone']
    #     try:
    #         # Преобразуем номер для региона RU
    #         parsed_phone = parse(str(phone), "RU")
    #         if not is_valid_number(parsed_phone):
    #             raise forms.ValidationError(
    #                 'Введите корректный номер телефона (например, +7XXXXXXXXXX или 8XXXXXXXXXX).'
    #             )
    #         return str(phone)  # Возвращаем номер как строку
    #     except NumberParseException:
    #         raise forms.ValidationError(
    #             'Введите корректный номер телефона (например, +7XXXXXXXXXX или 8XXXXXXXXXX).'
    #         )