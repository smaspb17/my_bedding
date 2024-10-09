from django.shortcuts import render, get_object_or_404

from shop.models import Product, Category


def catalog_list(request):
    cats = Category.objects.filter(level=0)
    return render(request, 'shop/category/list.html',
                  {'cats': cats})


def product_list(request, cat_slug=None):
    products = Product.objects.filter(is_available=True)
    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        products = products.filter(category=category)
        return render(request, 'shop/product/list.html',
                      {'products': products, 'category': category})
    return render(request, 'shop/product/list.html',
                  {'products': products})


def product_detail(request, cat_slug, product_id):
    category = get_object_or_404(Category, slug=cat_slug)
    product = get_object_or_404(Product, category=category,
                                id=product_id, is_available=True)
    return render(request, 'shop/product/detail.html',
                  {'category': category, 'product': product})


def test_view(request):
    product_1 = Product.objects.get(id=1)
    return render(request, 'shop/product/test.html',
                  {'product_1': product_1})
