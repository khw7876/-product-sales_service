from functools import partial
from product.serializers import ProductSerializer
from product.models import Product as ProductModel

def create_product(create_data, user):
    create_data["user"] = user
    product_serializer = ProductSerializer(data = create_data)
    product_serializer.is_valid(raise_exception=True)
    product_serializer.save()

def read_product():
    all_product = ProductModel.objects.all()
    product_serializer = ProductSerializer(all_product, many = True).data
    return product_serializer

def update_product(update_data, product_id):
    update_product_obj = ProductModel.objects.get(id=product_id)
    product_serializer = ProductSerializer(update_product_obj, update_data, partial = True)
    product_serializer.is_valid(raise_exception=True)
    product_serializer.save()

def delete_product(product_id):
    delete_product_obj = ProductModel.objects.get(id=product_id)
    delete_product_obj.delete()

def check_is_admin(user):
    if user.is_admin == True:
        return True
    return False