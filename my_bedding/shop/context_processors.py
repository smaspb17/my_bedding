from django.conf import settings

from shop.models import Category


def site_name(request):
    return {
        'site_name': settings.SITE_NAME,
    }


def category_list(request):
    categories = Category.objects.filter(level=0)
    return {'categories': categories}
