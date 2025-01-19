from decimal import Decimal

import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse

from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    # получить из сессии id заказа, добавленного туда ранее при его
    # создании в представлении order_create
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        )
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )
        total_cost_after_discount = order.total_cost_after_discount
        # данные для сеанса платежа Stripe
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [
                {
                    'price_data': {
                        'unit_amount': int(total_cost_after_discount * Decimal('100')),
                        'currency': 'rub',
                        'product_data': {'name': f'Оплата заказа № {order_id} от '
                                                 f'{order.create_date.strftime("%d.%m.%Y")}'},
                    },
                    'quantity': 1,
                }
            ],
        }
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)


def payment_completed(request):
    order_id = request.session.get('order_id', None)
    # request.session['redirect_source'] = 'payment_completed'
    return render(request, 'payment/completed.html',
                  {'order_id': order_id})
    # return redirect('orders:order_status', order_id=order_id)


def payment_canceled(request):
    order_id = request.session.get('order_id', None)
    # request.session['redirect_source'] = 'payment_canceled'
    return render(request, 'payment/canceled.html',
                  {'order_id': order_id})
    # return redirect('orders:order_status', order_id=order_id)
