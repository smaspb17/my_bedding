from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey

from . import choices

User = get_user_model()


class Category(MPTTModel):
    """Модель категории товара"""
    parent = TreeForeignKey(
        'self', on_delete=models.PROTECT,
        null=True, blank=True, related_name='children',
        db_index=True, verbose_name='Родительская категория')
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Слаг'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
    )
    logo = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name='Логотип',
    )

    class MPTTMeta:
        order_insertion_by = ['-id']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.title


class ProductSize(models.Model):
    """Модель размеров товаров"""
    title = models.CharField(
        max_length=100,
        verbose_name='Размер товара'
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name='sizes_by_cat',
        verbose_name='Категория'
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=100
    )
    logo = models.ImageField(
        upload_to='product_sizes/',
        blank=True,
        null=True,
        verbose_name='Картинка'
    )

    class Meta:
        verbose_name = 'Размер товара'
        verbose_name_plural = 'Размеры товаров'

    def __str__(self):
        return self.title


class ArticleSizeQuantityPrice(models.Model):
    """Модель размеров, количеств и цен у артикулов товара"""
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Товар',
    )
    article = models.PositiveIntegerField(
        unique=True,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(
                1000000, 'Артикул от 1 000 000'),
            MaxValueValidator(
                9999999, 'Артикул до 10 000 000'),
        ],
        verbose_name='Артикул',
    )
    size = models.ForeignKey(
        ProductSize,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Размер',
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Цена',
    )
    quantity = models.PositiveSmallIntegerField(
        default=0, verbose_name='Количество', validators=[MaxValueValidator(
            10000, 'Количество до 10 000 шт.'
        )]
    )
    equipment = models.TextField(
        verbose_name='Комплектация',
        help_text='Каждый элемент комплекта пишите на отдельной строке, '
                  'например:<br>Простыня без резинки (200х220 см) — 1 шт.'
                  '<br>Наволочки (50x70 см) — 2 шт.',
        blank=True,
        null=True,
    )
    shipping_weight = models.CharField(
        max_length=100,
        verbose_name='Упаковка',
        choices=choices.SHIPPING_WEIGHT,
        blank=True,
        null=True,
    )
    gross_weight = models.DecimalField(
        max_length=100,
        max_digits=5,
        verbose_name='Вес с упаковкой, кг',
        blank=True,
        null=True,
        decimal_places=1,
    )

    class Meta:
        verbose_name = 'Артикул'
        verbose_name_plural = ('Артикулы')

    def __str__(self):
        return (f"№ {self.article} ({self.product.title})")

    # def clean(self):
    #     super().clean()
    #     if self.product.category.slug == 'prostyni' and :
    #         raise ValidationError(
    #             'Выберите только один размер: либо размер простыни, '
    #             'либо размер простыни на резинке.'
    #         )
    #     if not self.size and not self.size_elastic:
    #         raise ValidationError(
    #             'Необходимо выбрать один размер: '
    #             'либо размер простыни, '
    #             'либо размер простыни на резинке.'
    #             )


class Product(models.Model):
    """Модель товара"""
    category = TreeForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категории',
    )
    title = models.CharField(
        unique=True,
        max_length=100,
        verbose_name='Название',
    )
    # slug = models.SlugField(
    #     max_length=100,
    #     unique=True,
    #     verbose_name='Слаг',
    # )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    care = models.TextField(
        verbose_name='Уход',
        blank=True,
        null=True,
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='В продаже',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлен'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']

    def __str__(self):
        return f"{self.title} (id {self.id})"

    def clean(self):
        super().clean()
        if self.category.children.exists():
            raise ValidationError(
                'У выбранной вами категории есть подкатегории. '
                'Выберите одну из них.'
                )


class ProductParam(models.Model):
    """Модель параметров товара"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='parameters',
        verbose_name='Товар'
    )
    color = models.CharField(
        max_length=100,
        choices=choices.COLOR,
        verbose_name='Цвет',
        null=True,
    )
    composition = models.CharField(
        max_length=100,
        choices=choices.COMPOSITION,
        verbose_name='Состав',
        null=True,
    )
    design = models.CharField(
        max_length=100,
        choices=choices.DESIGN,
        verbose_name='Дизайн',
        null=True,
    )
    material = models.CharField(
        max_length=100,
        choices=choices.MATERIAL,
        verbose_name='Материал',
        null=True,
    )
    density = models.CharField(
        max_length=100,
        choices=choices.DENSITY,
        verbose_name='Плотность',
        null=True,
    )
    washing_mode = models.CharField(
        max_length=100,
        choices=choices.WASHING_MODE,
        verbose_name='Режим стирки',
        null=True
    )
    type_of_sheet = models.CharField(
        max_length=100,
        choices=choices.TYPE_BED_SHEET,
        verbose_name='Вид простыни (комплекты и простыни)',
        blank=True, null=True,
    )
    presence_of_embroidery = models.CharField(
        max_length=100,
        choices=choices.TOWEL_PRESENCE_OF_EMBROIDERY,
        verbose_name='Наличие вышивки (полотенца)',
        blank=True, null=True,
    )
    filler = models.CharField(
        max_length=100,
        choices=choices.BEDSPREAD_FILLER,
        verbose_name='Наполнитель (покрывала)',
        blank=True, null=True,
    )

    def __str__(self):
        return f"{self.product.title} (id {self.product.id})"

    class Meta:
        verbose_name = 'Параметры товара'
        verbose_name_plural = 'Параметры товаров'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/',
        verbose_name='Фото'
    )
    size = models.CharField(
        max_length=10,
        choices=(('100x100', '100x100'), ('450x450', '450x450'),
                 ('800x800', '800x800'), ('1000x1000', '1000x1000')),
        verbose_name='Размер',
    )

    class Meta:
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товара'

    def __str__(self):
        return f"{self.product.title} (id {self.product.id})"