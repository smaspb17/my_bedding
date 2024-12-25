from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код')
    valid_from = models.DateTimeField(verbose_name='Начало')
    valid_to = models.DateTimeField(verbose_name='Окончание')
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)],
        help_text='Процентное значение (от 0 до 100)',
        verbose_name='Скидка'
    )
    active = models.BooleanField(verbose_name='Активен')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code

    # @staticmethod
    # def clear(request):
    #     """Удаление купона из сессии"""
    #     request.session['coupon_id'] = None
