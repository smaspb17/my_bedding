import locale

from django import template
from datetime import datetime

from coupons.models import Coupon


register = template.Library()


@register.simple_tag(takes_context=True)
def discount_percentage(context):
    request = context['request']  # Получаем request из контекста
    if 'coupon_id' in request.session and request.session['coupon_id'] is not None:
        coupon_id = request.session['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        result = coupon.discount
    else:
        result = 0
    return result


# @register.filter
# def image_size(value, arg=''):
#     """
#     Фильтр для получения фото с нужным разрешением.
#     Использование:
#     {{ p.product_images|image_size:"480x480" }}
#     """
#     return value.filter(size=arg)


@register.filter
def format_price(value):
    try:
        # Преобразуем строку в число с плавающей точкой
        value = int(value)
        # Форматируем значение как число с двумя знаками после запятой
        return f"{value:,}".replace(",", " ")
    except (ValueError, TypeError):
        return '0'


@register.filter
def pluralize_ru(value, arg=''):
    """
    Фильтр для склонения слов во множественном числе в русском языке.
    Использование:
    {{ total_items|pluralize_ru:"товар,товара,товаров" }}
    """
    words = arg.split(',')
    if len(words) != 3:
        raise ValueError(
            'Аргумент фильтра должен содержать 3 слова, разделенных запятыми'
            )
    value = abs(int(value))
    if value % 10 == 1 and value % 100 != 11:
        return f"{value} {words[0]}"
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return f"{value} {words[1]}"
    else:
        return f"{value} {words[2]}"


# Список месяцев на русском языке
MONTHS_RU = [
    'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
    'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
]


@register.filter
def format_date_rus(value):
    if isinstance(value, datetime):
        day = value.day
        month = MONTHS_RU[value.month - 1]  # Месяцы начинаются с 0
        year = value.year
        return f"{day} {month} {year} г."
    return value