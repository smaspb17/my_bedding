from decimal import Decimal

from django.conf import settings
from django.contrib import messages

from shop.models import Product, ArticleSizeQuantityPrice


class Cart:
    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, article_obj):
        """Добавление артикула в корзину (сессию)
         или увеличение количества товаров на 1."""
        article_num = str(article_obj.article)
        price = article_obj.price
        if article_num not in self.cart:
            self.cart[article_num] = {'quantity': 1, 'price': price}
        else:
            self.cart[article_num]['quantity'] += 1
        self.save()

    def reduce(self, article_obj):
        """Уменьшение количества товаров на 1."""
        article_num = str(article_obj.article)
        new_quantity = self.cart[article_num]['quantity'] - 1
        if new_quantity > 0:
            self.cart[article_num]['quantity'] = new_quantity
            self.save()
        else:
            self.remove(article_num)

    def update(self, article_obj, quantity):
        """Обновление количества товаров в ручную"""
        article_num = str(article_obj.article)
        if quantity > 0:
            self.cart[article_num]['quantity'] = quantity
            self.save()
        else:
            self.remove(article_num)

    def remove(self, article_num):
        """Удаление товара из корзины"""
        article_num = str(article_num)
        if article_num in self.cart:
            del self.cart[article_num]
            self.save()

    def get_quantity(self, article_obj):
        article_num = str(article_obj.article)
        return self.cart[article_num]['quantity']

    def __iter__(self):
        article_nums = [item for item in self.cart.keys()]
        article_objs = ArticleSizeQuantityPrice.objects.filter(article__in=article_nums)
        cart = self.cart.copy()
        for article_obj in article_objs:
            article_num = str(article_obj.article)
            cart[article_num]['total_price'] = cart[article_num]['quantity'] * cart[article_num]['price']
            cart[article_num]['article'] = article_obj
            cart[article_num]['product'] = article_obj.product
        for item in cart.values():
            yield item

    def save(self):
        """Пометка сеанса как измененного для его сохранения"""
        self.session.modified = True



session = {'cart': {
    '5': {'price': Decimal('200.00'), 'product': '<Product: Кеды>',
          'quantity': 1, 'total_price': Decimal('200.00'),
          'update_quantity_form': '<CartAddProductForm                       '
                                  '   bound=False, valid: Unknown, fields: ('
                                  'quantity;override)>'}},
    'order_id': 76}
