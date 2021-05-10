from mainapp.models import Product, AttributeValue


def add_filter(self, name, value):
    if name not in self.filter_set.keys() and self.founded_items:
        result = AttributeValue.objects.none()
        for item in self.founded_items:
            founded_product = AttributeValue.objects.filter(
                attribute_id=name,
                product_id=item['product_id'],
                value=value
            )
            result = result | founded_product if founded_product else result
            self.filter_set[name] = []
            self.filter_set[name].append(value)
        return result.values('product_id')

    elif name in self.filter_set.keys() and not self.founded_items:
        buffer = AttributeValue.objects.filter(attribute_id=name, value=value)
        buffer = buffer.values()
        result = AttributeValue.objects.none()
        for item in buffer:
            for key, values in self.filter_set.items():
                founded_product = AttributeValue.objects.filter(
                    attribute_id=key,
                    product_id=item['product_id_id'],
                    value=values
                )
                result = result | founded_product if founded_product else result
        return result.values('product_id')

    elif name in self.filter_set.keys() and self.founded_items:
        buffer = AttributeValue.objects.filter(attribute_id=name, value=value)
        buffer = buffer.values()
        result = AttributeValue.objects.none()
        for item in buffer:
            for key, values in self.filter_set.items():
                if key != name:
                    founded_product = AttributeValue.objects.filter(
                        attribute_id=key,
                        product_id=item['product_id_id'],
                        value=values
                    )
                    result = result | founded_product if founded_product else result
        return result.values('product_id')

    elif name not in self.filter_set.keys() and not self.founded_items:
        buffer = AttributeValue.objects.filter(attribute_id=name, value=value)
        result = buffer.values('product_id')
        self.filter_set[name] = []
        self.filter_set[name].append(value)
        return result.values('product_id')


def delete_filter(self, name, value):
    try:
        self.filter_set[name].remove(value)
        if not self.filter_set[name]:
            del self.filter_set[name]
        self.product_list = Product.objects.none()
        self.founded_items = AttributeValue.objects.none()
    except ValueError:
        pass
