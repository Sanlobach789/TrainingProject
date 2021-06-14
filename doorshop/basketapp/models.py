from django.db import models

from authapp.models import ShopUser

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)

    def get_items(self):
        baskets = Basket.objects.filter(user=self)
        return baskets

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(id=pk)
