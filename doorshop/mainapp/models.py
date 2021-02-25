from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(verbose_name='active', default=True)

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='img/products', blank=True)
    description = models.TextField(blank=True)
    short_desc = models.CharField(max_length=64, blank=True)
    price = models.DecimalField(max_length=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='active', default=True)

    def __str__(self):
        return f'{self.name} | {self.category.name}'
