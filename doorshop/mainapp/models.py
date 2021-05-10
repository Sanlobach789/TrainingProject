from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Название*")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(verbose_name='active', default=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="Родительская категория*")

    class Meta:
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return f'{self.name}'


class ProductAttributes(models.Model):
    name = models.CharField(max_length=64, unique=False, verbose_name="Название*")
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                    verbose_name="Категория*", related_name='category_attributes')

    class Meta:
        verbose_name_plural = 'Доступные атрибуты товаров'

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


class AttributeValue(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_id = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE, verbose_name="Атрибут")
    value = models.CharField(max_length=40, blank=True, verbose_name="Значение")

    class Meta:
        verbose_name_plural = 'Атрибуты товаров'

    def get_category_attributes(product_id):
        product_category = Product.objects.get(id=product_id).category_id
        category_attributes = ProductAttributes.category_attributes(product_category)
        return category_attributes

    def __str__(self):
        return f'{self.attribute_id}'


# class FilteredProductList:
#     filter_set = {}
#     founded_items = AttributeValue.objects.none()
#
#
#     def simple_filter(attr_id, values, founded_products=None):
#         result = AttributeValue.objects.none()
#         if not founded_products:
#             for val in values:
#                 buffer = AttributeValue.objects.filter(attribute_id=attr_id, value=val)
#                 result = result | buffer
#             return result
#         else:
#             for item in founded_products.values('product_id'):
#                 for val in values:
#                     buffer = AttributeValue(
#                         attribite_id=attr_id,
#                         product_id=item['product_id'],
#                         value=val
#                     )
#                     result = result | buffer
#             return result
#
#     @staticmethod
#     def recurs_filter(filter_set, founded_products=None, counter=0):
#
#         if counter == len(filter_set):
#             return founded_products
#         else:
#             for key, values in filter_set:
#                 if founded_products:
#                     founded_products = simple_filter(attr_id=key, values=values, founded_products=founded_products)
#                     filter_set.pop(key)
#                     counter += 1
#                     recurs_filter(filter_set, founded_products, counter)
#                 else:
#                     founded_products = simple_filter(attr_id=key, values=values)
#                     filter_set.pop(key)
#                     counter += 1
#                     recurs_filter(filter_set, founded_products, counter)
#     # # def add_filter(self, name, value):
#     # #     if name not in self.filter_set.keys():
#     # #         self.filter_set[name] = []
#     # #     self.filter_set[name].append(value)
#     #
#     # def add_filter(self, name, value):
#     #     if name not in self.filter_set.keys() and self.founded_items:
#     #         result = AttributeValue.objects.none()
#     #         for item in self.founded_items:
#     #             founded_product = AttributeValue.objects.filter(
#     #                 attribute_id=name,
#     #                 product_id=item['product_id'],
#     #                 value=value
#     #             )
#     #             result = result | founded_product if founded_product else result
#     #         self.founded_items = result.values('product_id')
#     #         self.filter_set[name] = []
#     #         self.filter_set[name].append(value)
#     #         print(self.founded_items)
#     #         return self.founded_items
#     #
#     #     elif name in self.filter_set.keys() and not self.founded_items:
#     #         buffer = AttributeValue.objects.filter(attribute_id=name, value=value)
#     #         buffer = buffer.values()
#     #         result = AttributeValue.objects.none()
#     #         for item in buffer:
#     #             for key, values in self.filter_set.items():
#     #                 founded_product = AttributeValue.objects.filter(
#     #                     attribute_id=key,
#     #                     product_id=item['product_id_id'],
#     #                     value=values
#     #                 )
#     #                 result = result | founded_product if founded_product else result
#     #         self.founded_items = result.values('product_id')
#     #         print(self.founded_items)
#     #         return self.founded_items
#     #
#     #     elif name in self.filter_set.keys() and self.founded_items:
#     #         buffer = AttributeValue.objects.filter(attribute_id=name, value=value)
#     #         buffer = buffer.values('product_id')
#     #         result = buffer
#     #         print(self.filter_set)
#     #         for item in buffer:
#     #             for key, values in self.filter_set.items():
#     #                 if key != name:
#     #                     for val in values:
#     #                         founded_product = AttributeValue.objects.filter(
#     #                             attribute_id=key,
#     #                             product_id=item['product_id'],
#     #                             value=val
#     #                         )
#     #                         result = result | founded_product.values('product_id')
#     #         self.founded_items = self.founded_items | result.values('product_id')
#     #         self.filter_set[name].append(value)
#     #         print(self.founded_items)
#     #         return self.founded_items
#     #
#     #     elif name not in self.filter_set.keys() and not self.founded_items:
#     #         buffer = AttributeValue.objects.filter(attribute_id=name, value=value)
#     #         result = buffer.values('product_id')
#     #         self.founded_items = result.values('product_id')
#     #         self.filter_set[name] = []
#     #         self.filter_set[name].append(value)
#     #         print(self.founded_items)
#     #         return self.founded_items
#     #
#     # def delete_filter(self, name, value):
#     #     try:
#     #         self.filter_set[name].remove(value)
#     #         if not self.filter_set[name]:
#     #             del self.filter_set[name]
#     #         result = Product.objects.none()
#     #         for item in self.founded_items:
#     #             for key, values in self.filter_set.items():
#     #                 for val in values:
#     #                     buffer = AttributeValue.objects.filter(
#     #                         attribute_id=key,
#     #                         product_id=item['product_id'],
#     #                         value=val
#     #                     )
#     #                     result = result | buffer if buffer else result
#     #         self.founded_items = result.values('product_id')
#     #         print(self.founded_items)
#     #         return self.founded_items
#     #     except ValueError:
#     #         pass
#
#     # @staticmethod
#     # def get_filter_list(key, values, founded_items=None):
#     #     result = AttributeValue.objects.none()
#     #     # if not founded_items:
#     #     #     for val in values:
#     #     #         buffer = AttributeValue.objects.filter(attribute_id=key, value=val)
#     #     #         result = result | buffer
#     #     # else:
#     #     #     for val in values:
#     #     #         for item in founded_items.values('product_id'):
#     #     #             if item['attribute_id'] != key:
#     #     #                 buffer = AttributeValue.objects.filter(
#     #     #                     attribute_id=key,
#     #     #                     product_id=item['product_id'],
#     #     #                     value=val
#     #     #                 )
#     #     #                 result = result | buffer
#     #     #             else:
#     #     #                 buffer = AttributeValue.objects.filter(attribute_id=key, value=val)
#     #     #                 result = result | buffer
#     #     if founded_items:
#     #         for val in values:
#     #             for item in founded_items.values():
#     #                 if item['attribute_id_id'] == key:
#     #                     buffer = AttributeValue.objects.filter(attribute_id=key, value=val)
#     #                     result = result | buffer
#     #                 else:
#     #                     buffer = AttributeValue.objects.filter(
#     #                         attribute_id=key,
#     #                         product_id=item['product_id_id'],
#     #                         value=val
#     #                     )
#     #                     result = result | buffer if buffer else result
#     #     else:
#     #         for val in values:
#     #             buffer = AttributeValue.objects.filter(attribute_id=key, value=val)
#     #             result = result | buffer
#     #     return result
#     #
#     # def get_filtered_list(self):
#     #     for key, values in self.filter_set.items():
#     #         if self.founded_items:
#     #             self.founded_items = self.get_filter_list(key, values, self.founded_items)
#     #         else:
#     #             self.founded_items = self.get_filter_list(key, values)
#     #
#     #     for product_id in self.founded_items.values('product_id'):
#     #         self.product_list = self.product_list | Product.objects.filter(id=product_id['product_id'])
#     #
#     #     return self.product_list

class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/products', blank=True)

    class Meta:
        verbose_name_plural = 'Изображения товаров'
