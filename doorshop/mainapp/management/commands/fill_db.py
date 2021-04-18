from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product, ProductMeasure, ProductAttributes, AttributeValue
import json, os

JSON_PATH = 'mainapp/fixtures'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


def create_parent_category(id, name, description, is_active):
    parent = ProductCategory()
    parent.id = id
    parent.name = name
    parent.description = description
    parent.is_active = is_active
    parent.save()
    parent.parent_category = ProductCategory.objects.get(id=id)
    parent.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('mainapp_products')

        ProductCategory.objects.all().delete()
        create_parent_category(1, "Входные двери", "", True)
        create_parent_category(4, "Межкомнатные двери", "", True)
        for category in categories:
            parent_id = category["parent_category"]
            _parent_category = ProductCategory.objects.get(id=parent_id)
            category["parent_category"] = _parent_category
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            _category = ProductCategory.objects.get(id=category_name)
            product["category"] = _category
            measure_id = product["measure"]
            product["measure"] = ProductMeasure.objects.get(id=measure_id)
            new_product = Product(**product)
            new_product.save()

        attributes = load_from_json('products_attributes')
        ProductAttributes.objects.all().delete()
        for attr in attributes:
            category_id = attr["category_id"]
            attr["category_id"] = ProductCategory.objects.get(id=category_id)
            new_attr = ProductAttributes(**attr)
            new_attr.save()

        attr_values = load_from_json('attributes_values')
        AttributeValue.objects.all().delete()
        for attr in attr_values:
            attr["product_id"] = Product.objects.get(id=attr["product_id"])
            attr["attribute_id"] = ProductAttributes.objects.get(id=attr["attribute_id"])
            attr_value = AttributeValue(**attr)
            attr_value.save()
