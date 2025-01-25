from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from cart.cart import Cart
from shop.models import Product, Category


def catalog_list(request):
    cats = Category.objects.filter(level=0)
    return render(request, 'shop/category/list.html',
                  {'cats': cats})


def product_list(request, cat_slug=None):
    products = Product.objects.filter(is_available=True)
    cart = request.session.get('cart', {})
    context = {'products': products, 'cart': cart}

    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        descendant_categories = category.get_children()  # Получаем дочерние категории
        all_categories = [category] + list(descendant_categories)
        products = products.filter(category__in=all_categories)  # Фильтруем продукты по категориям
        context.update({'category': category, 'products': products})

        # Пагинация: 8 товаров на страницу
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)

    context.update({'products': page})

    return render(request, 'shop/product/list.html', context)




    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Проверка AJAX-запроса
    #     html = render_to_string('shop/product/_product_cards.html', context=context, request=request)
    #     return JsonResponse({'html': html, 'has_next': page.has_next()})





def product_detail(request, cat_slug, product_id):
    category = get_object_or_404(Category, slug=cat_slug)
    product = get_object_or_404(Product, category=category,
                                id=product_id, is_available=True)
    cart = request.session.get('cart', {})
    return render(request, 'shop/product/detail.html',
                  {'category': category, 'product': product, 'cart': cart})


def test_view(request):
    product_1 = Product.objects.get(id=1)
    return render(request, 'shop/product/test.html',
                  {'product_1': product_1})
