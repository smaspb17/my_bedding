from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model

from cart.cart import Cart
from coupons.models import Coupon
from .forms import OrderCreateForm
from .models import OrderItem, Order
from .tasks import order_created

User = get_user_model()


@never_cache
def order_create(request):
    cart = Cart(request)
    if not cart or len(cart) == 0:
        return redirect('cart:cart-detail')  # Перенаправление на страницу корзины
    cart_items = [item for item in cart]
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            user = request.user
            # if not user.is_authenticated:
            #     print('Не авторизован!!!')
            #     return JsonResponse({'authenticated': False}, status=401)
            order.user = user
            order.email = user.email
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    article=item['article'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            if request.session.get('coupon_id') is not None:
                order.coupon = Coupon.objects.get(id=request.session['coupon_id'])
            order.total_cost = order.get_total_cost()
            order.discount_percentage = order.get_discount_percentage()
            order.discount = order.get_discount()
            order.total_cost_after_discount = order.get_total_cost_after_discount()
            order.save()
            cart.clear()
            request.session['coupon_id'] = None
            # создание асинхронного задания-отправка email
            order_created.delay(order.id)
            return redirect('orders:order_status', order.id)

        else:
            return render(
                request, 'orders/create.html',
                {'form': form, 'cart': cart, 'cart_items': cart_items})
    else:
        form = OrderCreateForm()
        return render(
            request, 'orders/create.html',
            {
                'form': form,
                'cart': cart,
                'cart_items': cart_items,
            })


def order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    payment_status = 'Оплачен' if order.payment else 'Не оплачен'
    status = order.get_status_display()
    transport_company = order.get_transport_company_display()
    request.session['order_id'] = order.id
    redirect_source = request.session.pop('redirect_source', None)
    return render(request, 'orders/status.html',
                  {'order': order, 'order_items': order_items,
                           'payment_status': payment_status,
                           'status': status,
                           'transport_company': transport_company,
                           'redirect_source': redirect_source})
