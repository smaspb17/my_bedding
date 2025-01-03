from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, \
    get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST

from coupons.forms import CouponForm
from coupons.models import Coupon
from shop.models import Product, ArticleSizeQuantityPrice
from .cart import Cart


@require_POST
def cart_add(request, article):
    article = get_object_or_404(ArticleSizeQuantityPrice, article=article)
    cart = Cart(request)
    cart.add(article_obj=article)
    # Проверяем, добавлен ли товар в корзину
    article_num = str(article.article)
    in_cart = article_num in cart.cart
    context = {'article': article.article, 'in_cart': in_cart}
    # Если товар добавлен в корзину, возвращаем ссылку на cart-detail с золотой иконкой
    # if in_cart:
    #     html = render_to_string('cart/partials/cart_added.html', context, request=request)
    # else:
    #     # Если по какой-то причине товар не добавлен, возвращаем форму с серой иконкой
    #     html = render_to_string('cart/partials/cart_form.html', context, request=request)
    # return HttpResponse(html)
    return JsonResponse({'message': 'Товар добавлен в корзину', 'success': True})


def cart_increase(request, article):
    """Увеличение количества товаров в корзине на 1."""
    article = get_object_or_404(ArticleSizeQuantityPrice, article=article)
    cart = Cart(request)
    if cart.get_quantity(article) < 10:
        cart.add(article)
    return JsonResponse({'quantity': cart.get_quantity(article)})


def cart_decrease(request, article):
    """Уменьшение количества товаров в корзине на 1."""
    article = get_object_or_404(ArticleSizeQuantityPrice, article=article)
    cart = Cart(request)
    cart.reduce(article)
    return JsonResponse({'quantity': cart.get_quantity(article)})


def update_quantity(request, article):
    """Обновление количества товаров в корзине в ручную"""
    article = get_object_or_404(ArticleSizeQuantityPrice, article=article)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        elif quantity > 10:
            quantity = 10
    except ValueError:
        quantity = 1
    cart.update(article, quantity)
    return JsonResponse({'quantity': cart.get_quantity(article)})


def cart_remove(request, article):
    cart = Cart(request)
    cart.remove(article)
    if not cart.cart:
        request.session['coupon_id'] = None
    # print(cart.cart)
    return JsonResponse({'message': 'Товар удален из корзины', 'success': True})


def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponForm()
    # if 'coupon_id' not in request.session:
    #     request.session['coupon_id'] = None
    context = {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form,
        # 'total_price': cart.get_total_price(),
        # 'discount': cart.get_discount(),
        # 'total_price_after_discount': cart.get_total_price_after_discount(),
        # 'current_path': request.path,
    }
    return render(request, 'cart/cart_detail.html', context)


# def cart_status(request):
#     """Возвращает список артикулов, находящихся в корзине."""
#     cart = Cart(request)
#     articles_in_cart = [item['article'] for item in cart]
#     return JsonResponse({'cart': articles_in_cart})


def get_discount(request):
    cart = Cart(request)
    discount = cart.get_discount()
    if not request.session.get('coupon_id'):
        discount_percentage = 0
        discount_code = ''
    else:
        coupon_id = request.session['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        discount_percentage = coupon.discount
        discount_code = coupon.code
    return JsonResponse({'discount': discount,
                         'discount_percentage': discount_percentage,
                         'discount_code': discount_code})
