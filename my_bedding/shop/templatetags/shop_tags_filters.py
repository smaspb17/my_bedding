from django import template

register = template.Library()


@register.filter
def image_size(value, arg=''):
    """
    Фильтр для получения фото с нужным разрешением.
    Использование:
    {{ p.product_images|image_size:"480x480" }}
    """
    return value.filter(size=arg)


@register.filter
def format_price(value):
    try:
        # Преобразуем строку в число с плавающей точкой
        value = int(value)
        # Форматируем значение как число с двумя знаками после запятой
        return f"{value:,}".replace(",", " ")
    except (ValueError, TypeError):
        return '0'