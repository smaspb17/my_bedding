from django.contrib import admin
# from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

from shop.models import (
    Category, Product, ProductImage, ProductSize, ArticleSizeQuantityPrice,
    ProductParam)


# PARAMS = {1: 'color', 2: 'design', 3: 'material', 4: 'washing_mode',
#           5: 'density', 6: 'type_of_sheet', 7: 'towel_material',
#           8: 'towel_density', 9: 'presence_of_embroidery',
#           10: 'filler'}
#
# PARAMS_BY_CAT = {
#     'komplekty-postelnogo-belya': [1, 2, 3, 4, 5, 6],
#     'prostyni': [1, 2, 3, 4, 5, 6],
#     'prostyni-bez-rezinki': [1, 2, 3, 4, 5, 6],
#     'prostyni-s-rezinkoj': [1, 2, 3, 4, 5, 6],
#     'navolochki': [1, 2, 3, 4, 5],
#     'pododeyalniki': [1, 2, 3, 4, 5],
#     'polotenca': [1, 2, 7, 4, 8, 9],
#     'mahrovye-polotenca': [1, 2, 7, 4, 8, 9],
#     'vafelnye-polotenca': [1, 2, 7, 4, 8, 9],
#     'pledy-i-pokryvala': [1, 3, 4, 10],
#     'detskie-ugolki': [7],
#     'detyam': [1, 2, 3, 4, 5],
# }


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    # fields = ['parent', 'title', 'slug', 'description', 'logo']
    # list_display = ['id', 'title', 'slug', 'description']
    # list_display_links = ['id', 'title']
    # search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    fields = ['image']
    extra = 7  # Количество пустых форм для добавления


class ProductParamAdmin(admin.StackedInline):
    model = ProductParam
    fields = [
        'color', 'composition', 'design', 'material', 'density',
        'washing_mode', 'type_of_sheet', 'presence_of_embroidery', 'filler']


# class ParamBedLinenAdmin(admin.StackedInline):
#     model = ParamBedLinen
#     fields = ['color', 'design', 'material', 'washing_mode', 'density',
#               'type_of_sheet']
#
#
# class ParamPillowcaseAdmin(admin.StackedInline):
#     model = ParamPillowcase
#     fields = ['color', 'design', 'material', 'washing_mode', 'density']
#
#
# class ParamBedSheetAdmin(admin.StackedInline):
#     model = ParamBedSheet
#     fields = ['color', 'design', 'material', 'washing_mode', 'density',
#               'type_of_sheet']
#
#
# class ParamDuvetCoverAdmin(admin.StackedInline):
#     model = ParamDuvetCover
#     fields = ['color', 'design', 'material', 'washing_mode', 'density',]
#
#
# class ParamTowelAdmin(admin.StackedInline):
#     model = ParamTowel
#     fields = ['color', 'design', 'material', 'washing_mode', 'density',
#               'presence_of_embroidery']
#
#
# class ParamBedSpreadAdmin(admin.StackedInline):
#     model = ParamBedSpread
#     fields = ['color', 'material', 'washing_mode', 'filler']


# class BaseSizeQuantityPriceAdmin(admin.TabularInline):
#     fields = ['size', 'price', 'quantity']


# class ProductBedLinenSizeQuantityPriceAdmin(BaseSizeQuantityPriceAdmin):
#     fields = ['size', 'price', 'quantity']
#     model = ProductBedLinenSizeQuantityPrice
#
#
# class ProductPillowcaseSizeQuantityPriceAdmin(BaseSizeQuantityPriceAdmin):
#     model = ProductPillowcaseSizeQuantityPrice
#
#
# class ProductBedSheetSizeQuantityPriceAdmin(BaseSizeQuantityPriceAdmin):
#     fields = ['size', 'size_elastic', 'price', 'quantity']
#     model = ProductBedSheetSizeQuantityPrice
#
#
# class ProductDuvetCoverSizeQuantityPriceAdmin(BaseSizeQuantityPriceAdmin):
#     model = ProductDuvetCoverSizeQuantityPrice
#
#
# class ProductTowelSizeQuantityPriceAdmin(BaseSizeQuantityPriceAdmin):
#     fields = ['size_waffle', 'size_terry', 'price', 'quantity']
#     model = ProductTowelSizeQuantityPrice
#
#
# class ProductBedSpreadSizeQuantityPriceAdmin(BaseSizeQuantityPriceAdmin):
#     model = ProductBedSpreadSizeQuantityPrice


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    fields = ['category', 'title', 'description', 'logo']
    list_display = ['title', 'category', 'description', 'logo']
    list_filter = ['category']
    list_editable = ['category', 'description']


class ArticleSizeQuantityPriceInline(admin.StackedInline):
    fields = ['article', 'size', 'price', 'quantity', 'equipment',
              'shipping_weight', 'gross_weight', ]
    model = ArticleSizeQuantityPrice
    extra = 3
    # formset = ProductSizeQuantityPriceInlineFormSet

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Фильтруем поле size в зависимости от категории продукта
        if obj:
            formset.form.base_fields['size'].queryset = ProductSize.objects.filter(
                category=obj.category)
        return formset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'care', 'is_available', 'category',
              'created', 'updated']
    readonly_fields = ['created', 'updated']
    list_display = ['id', 'title', 'category', 'is_available']
    list_display_links = ['id', 'title',]
    search_fields = ['title']
    list_editable = ['category', 'is_available',]
    save_on_top = True
    list_filter = ['category']
    inlines = [ProductParamAdmin, ArticleSizeQuantityPriceInline,
               ProductImageAdmin]
