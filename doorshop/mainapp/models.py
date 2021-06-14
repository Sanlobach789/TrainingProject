from PIL import Image
from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Название*")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(verbose_name='active', default=True)
    is_parent_category = models.BooleanField(verbose_name='Является родительской категорией', default=False)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="Родительская категория*")

    class Meta:
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save()
        if self.is_parent_category:
            self.parent_category = self
            return super(ProductCategory, self).save(*args, **kwargs)


class ProductAttributes(models.Model):
    name = models.CharField(max_length=64, unique=False, verbose_name="Название*")
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                    verbose_name="Категория*", related_name='category_attributes')

    class Meta:
        verbose_name_plural = 'Доступные атрибуты товаров'

    @staticmethod
    def category_attributes(category_id):
        return ProductAttributes.objects.filter(category_id=category_id)

    def __str__(self):
        return f'{self.name}'


class ProductMeasure(models.Model):
    name = models.CharField(max_length=10, verbose_name="Название*")

    class Meta:
        verbose_name_plural = 'Единицы измерения товаров'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название*")
    image = models.ImageField(upload_to='img/products', blank=True,
                              default='img/product-img/product_default.jpg', verbose_name="Главное изображение")
    description = models.TextField(blank=True, verbose_name="Описание")
    short_desc = models.CharField(max_length=64, blank=True, verbose_name="Короткое описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Цена*")
    quantity = models.PositiveIntegerField(default=0, verbose_name="В наличие")
    measure = models.ForeignKey(ProductMeasure, on_delete=models.CASCADE, verbose_name="Ед. изм.*")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="Категория*")
    is_active = models.BooleanField(verbose_name='Доступна на сайте?', default=True)

    class Meta:
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name}'

    def get_price(self):
        return f'{self.price}'

    def get_remainder(self):
        return f'{self.quantity}'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class AttributeValue(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_id = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE, verbose_name="Атрибут")
    value = models.CharField(max_length=40, verbose_name="Значение")

    class Meta:
        verbose_name_plural = 'Атрибуты товаров'

    def get_category_attributes(product_id):
        product_category = Product.objects.get(id=product_id).category_id
        category_attributes = ProductAttributes.category_attributes(product_category)
        return category_attributes

    def __str__(self):
        return f'{self.attribute_id}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/products', blank=True)

    class Meta:
        verbose_name_plural = 'Изображения товаров'


class SortValues(models.Model):
    name = models.CharField(max_length=32, unique=True)
    value = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = 'Варианты сортировки'

    def __str__(self):
        return f'{self.name}'


class SocialUrls(models.Model):
    WHATSAPP = 'Whatsapp'
    TELEGRAM = 'Telegram'
    INSTAGRAM = 'instagram'
    VK = 'VK'

    SOCIAL_CHOICES = {
        (WHATSAPP, 'Whatsapp'),
        (TELEGRAM, 'Telegram'),
        (INSTAGRAM, 'instagram'),
        (VK, 'VK'),
    }

    name = models.CharField(max_length=10, choices=SOCIAL_CHOICES, verbose_name='Соц. сеть')
    url_path = models.TextField(blank=True, verbose_name='Ссылка')

    class Meta:
        verbose_name_plural = 'Ссылки на соц сети'

    def __str__(self):
        return f'{self.url_path}'
