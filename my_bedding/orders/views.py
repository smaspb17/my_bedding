from django.shortcuts import render

from cart.cart import Cart
from coupons.models import Coupon
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order


def order_create(request):
    cart = Cart(request)
    cart_items = [item for item in cart]
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    article=item['article'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            if request.session['coupon_id'] is not None:
                order.coupon = Coupon.objects.get(id=request.session['coupon_id'])
            order.total_cost = order.get_total_cost()
            order.discount_percentage = order.get_discount_percentage()
            order.discount = order.get_discount()
            order.total_cost_after_discount = order.get_total_cost_after_discount()
            order.save()
            cart.clear()
            request.session['coupon_id'] = None
            return render(request, 'orders/created.html',
                          {'order': order})

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
