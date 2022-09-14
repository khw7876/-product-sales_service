from product.serializers import ProductSerializer

def create_product(create_data, user):
    create_data["user"] = user
    product_serializer = ProductSerializer(data = create_data)
    product_serializer.is_valid(raise_exception=True)
    product_serializer.save()
