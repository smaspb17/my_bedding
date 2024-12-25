import re
import requests
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from cart.cart import Cart
from coupons.models import Coupon
from . import choices
from shop.models import ArticleSizeQuantityPrice
from .validators import (
    validate_russian_phone,
    validate_first_name,
    validate_last_name,
    validate_user_address,
    validate_pickup_point_address
)


class Order(models.Model):
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.PROTECT,
    #     related_name='orders',
    #     verbose_name='Покупатель'
    # )
    first_name = models.CharField(
        max_length=50,
        validators=[validate_first_name],
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=50,
        validators=[validate_last_name],
        verbose_name='Фамилия',
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=12,  # Для номеров типа +7XXXXXXXXXX
        validators=[validate_russian_phone],
        # unique=True,
        # blank=True,
        # null=True,
    )
    email = models.EmailField(
        verbose_name='E-mail',
    )
    # index = models.CharField(
    #     max_length=6,
    #     verbose_name='Индекс доставки',
    # )
    user_address = models.CharField(
        max_length=250,
        verbose_name='Адрес покупателя',
        validators=[validate_user_address],
        # help_text='Указывайте домашний адрес либо адрес пункта выдачи для службы доставки'
    )
    pickup_point_address = models.CharField(
        max_length=250,
        verbose_name='Адрес ПВЗ',
        validators=[validate_pickup_point_address],
        # help_text='Указывайте домашний адрес либо адрес пункта выдачи для службы доставки'
    )
    transport_company = models.CharField(
        max_length=50,
        choices=choices.TRANSPORT_COMPANY,
        default='Russian post',
        verbose_name='ТК'
    )
    comment = models.TextField(
        max_length=250,
        verbose_name='Комментарий к заказу',
        blank=True,
        null=True,
    )
    create_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    status = models.CharField(
        max_length=100,
        choices=choices.ORDER_STATUS,
        default='Created',
        verbose_name='Статус заказа',
    )
    payment = models.CharField(
        max_length=100,
        choices=choices.PAYMENT_STATUS,
        default='Not paid',
        verbose_name='Оплачен',
    )
    # stripe_id = models.CharField(
    #     max_length=250, blank=True
    # )
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Купон',
    )
    discount_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Скидка %',
    )
    total_cost = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100000000)],
        verbose_name='Стоимость товара руб.',
        null=True,
    )
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100000000)],
        verbose_name='Скидка руб.',
        default=0,
    )
    delivery_cost = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100000000)],
        verbose_name='Доставка руб.',
        default=0,
    )
    total_cost_after_discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100000000)],
        verbose_name='Итоговая стоимость руб.',
        null=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=['-create_date']),
        ]
        ordering = ['-create_date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.id}'

    def clean(self):
        super().clean()
        user_postal_code = re.match(r"(\d{6})", self.user_address)
        pickup_point_postal_code = re.match(r"(\d{6})", self.pickup_point_address)
        if pickup_point_postal_code and user_postal_code:
            if user_postal_code.group(1) != pickup_point_postal_code.group(1):
                raise ValidationError({'user_address': "Индекс адреса не совпадает с индексом пункта доставки"})

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount_percentage(self):
        if self.coupon:
            return self.coupon.discount
        return 0

    def get_discount(self):
        total_cost = self.get_total_cost()
        if self.discount_percentage:
            return total_cost * (self.discount_percentage / Decimal(100))
        return 0

    def get_total_cost_after_discount(self):
        total_cost = self.get_total_cost()
        discount = self.get_discount()
        delivery_cost = self.delivery_cost
        return total_cost - discount + delivery_cost

    # def get_stripe_url(self):
    #     if not self.stripe_id:
    #         # нет ассоциированных платежей
    #         return ''
    #     if '_test_' in settings.STRIPE_SECRET_KEY:
    #         # путь stripe для тестовых платежей
    #         path = '/test/'
    #     else:
    #         # пусть stripe для настоящих платежей
    #         path = '/'
    #     return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ',
    )
    article = models.ForeignKey(
        ArticleSizeQuantityPrice,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Артикул'
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Цена'
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество'
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
