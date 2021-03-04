from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(verbose_name='active', default=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class ProductAttributes(models.Model):

    class DataTypes(models.TextChoices):
        TEXT = 'Текст'
        INTEGER = 'Целое число'
        DECIMAL = 'Число с запятой'

    name = models.CharField(max_length=64, unique=True)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    data_type = models.CharField(max_length=15, choices=DataTypes.choices, default=DataTypes.TEXT)

    def __str__(self):
        return f'{self.name} | {self.category_id}'

    def get_category_attributes(product):
        attributes = ProductAttributes.objects.filter(category_id=product.category)
        return attributes


class ProductMeasure(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='img/products', blank=True, default='img/product-img/product_default.jpg')
    description = models.TextField(blank=True)
    short_desc = models.CharField(max_length=64, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    measure = models.ForeignKey(ProductMeasure, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='active', default=True)

    def __str__(self):
        return f'{self.name} | {self.category.name}'


class AttributeValue(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_id = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE)
    value = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f'{self.attribute_id}'
