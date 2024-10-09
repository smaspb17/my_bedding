# from django.contrib import admin
# from django import forms
# from .models import ProductSizeQuantityPrice, ProductSize, Product


# class ProductSizeQuantityPriceInlineFormSet(forms.BaseInlineFormSet):
#     def get_form_kwargs(self, index):
#         kwargs = super().get_form_kwargs(index)
#         if self.instance.pk:
#             # Получаем продукт и его категорию
#             product = self.instance
#             category = product.category
#             # Фильтруем размеры по категории
#             kwargs['size_queryset'] = ProductSize.objects.filter(category=category)
#         else:
#             kwargs['size_queryset'] = ProductSize.objects.none()
#         return kwargs

