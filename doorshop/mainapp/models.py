from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Название*")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(verbose_name='active', default=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="Родительская категория*")

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class ProductAttributes(models.Model):

    name = models.CharField(max_length=64, unique=False, verbose_name="Название*")
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="Категория*")

    def __str__(self):
        return f'{self.name}'


class ProductMeasure(models.Model):
    name = models.CharField(max_length=10, verbose_name="Название*")

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

    def __str__(self):
        return f'{self.name}'

    def get_price(self):
        return f'{self.price}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/products', blank=True)


class AttributeValue(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_id = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE, verbose_name="Атрибут")
    value = models.CharField(max_length=40, blank=True, verbose_name="Значение")

    def __str__(self):
        return f'{self.attribute_id}'


