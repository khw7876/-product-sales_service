from product.serializers import ProductSerializer, PayHistorySerializer
from product.models import Product as ProductModel, PayHistory as PayHistoryModel

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

def get_total_price(pay_data, product_id):
    product_count = pay_data["count"]
    product_obj = ProductModel.objects.get(id=product_id)

    total_price = int(product_count) * int(product_obj.price) + int(product_obj.delivery_fee)
    return total_price

def check_user_can_pay(total_price, user):
    if user.point > total_price:
        return True
    return False
    
def pay_user_point(total_price, user):
    user.point = int(user.point) - int(total_price)
    user.save()
    return user.point

def create_pay_history(pay_data, user, product_id, balance_point, total_price):
    pay_data["user"] = user.id
    pay_data["product"] = product_id
    pay_data["balance"] = balance_point
    pay_data["total_price"] = total_price
    pay_history_serializer = PayHistorySerializer(data=pay_data)
    pay_history_serializer.is_valid(raise_exception=True)
    pay_history_serializer.save()

def read_pay_history():
    all_pay_history = PayHistoryModel.objects.all()
    pay_history_serializer = PayHistorySerializer(all_pay_history, many=True).data
    return pay_history_serializer

def detail_read_pay_history(pay_history_id):
    pay_history_obj = PayHistoryModel.objects.get(id=pay_history_id)
    detail_pay_history_serializer = PayHistorySerializer(pay_history_obj).data
    return detail_pay_history_serializer


def refund_product(pay_history_id):
    pay_history_obj = PayHistoryModel.objects.get(id=pay_history_id)
    user = pay_history_obj.user
    user.point = int(user.point) + int(pay_history_obj.total_price)
    pay_history_obj.delete()
    user.save()

    return pay_history_obj.total_price, user.point
