from django.http import JsonResponse
from django.utils import timezone

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from .forms import CouponForm
from .models import Coupon


def coupon_apply(request):
    if request.method == 'POST':
        now = timezone.now()
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(
                    code__iexact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True,
                )
                discount_percentage = coupon.discount
                request.session['coupon_id'] = coupon.id
                return JsonResponse({'success': True,
                                     'message': 'Промокод применён',
                                     'code': code,
                                     'discount_percentage': discount_percentage,
                                     })
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
                return JsonResponse({'success': False, 'message': 'Промокод недействителен'})
        return JsonResponse({'success': False, 'message': 'Некорректный промокод'})


def coupon_remove(request):
    request.session['coupon_id'] = None
    return JsonResponse({'success': True, 'message': 'Промокод неактивен'})







