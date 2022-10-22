from typing import Union

from product.serializers import ProductSerializer, PayHistorySerializer
from product.models import Product as ProductModel, PayHistory as PayHistoryModel

from user.models import User


def create_product(create_data: dict, user: User):
    """
    관리자가 상품을 등록하는 service
    Args:
        create_data (dict): {
            "name" : "등록할 상품의 이름",
            "price" : "등록할 상품의 금액",
            "delivery_fee" : "등록할 상품의 배송비"
        }
        user (user): 로그인이 되어있는 User_obj
    """
    create_data["user"] = user
    product_serializer = ProductSerializer(data=create_data)
    product_serializer.is_valid(raise_exception=True)
    product_serializer.save()


def read_product():
    """
    등록된 상품들을 불러오는 service
    Returns:
        ProductSerializer: 저장되어있는 전체 ProductModel의 serializer
    """
    all_product = ProductModel.objects.all()
    product_serializer = ProductSerializer(all_product, many=True).data
    return product_serializer


def update_product(update_data: dict[str, Union[str, int]], product_id: int) -> None:
    """
    등록되어있는 상품의 id를 토대로 상품을 update하는 service
    Args:
        update_data (dict[str, Union[str, int]]): {
            "price" : "수정할 상품의 가격,
            "delivery_fee" : "수정할 상품의 배송비,
        }
        product_id (int): 수정할 상품의 id
    """
    update_product_obj = ProductModel.objects.get(id=product_id)
    product_serializer = ProductSerializer(
        update_product_obj, update_data, partial=True)
    product_serializer.is_valid(raise_exception=True)
    product_serializer.save()


def delete_product(product_id: int) -> None:
    """
    등록되어있는 상품의 id를 토대로 상품을 등록해제하는 service
    Args:
        product_id (int): _description_
    """
    delete_product_obj = ProductModel.objects.get(id=product_id)
    delete_product_obj.delete()


def check_is_admin(user: User) -> bool:
    """
    현재 서비스를이용하는 유저가 관리자인지를 체크하는 service
    Args:
        user (User): 로그인한 User_obj

    Returns:
        bool: 관리자라면 True, 일반유저라면 False
    """
    if user.is_admin == True:
        return True
    return False


def get_total_price(product_count: int, product_id: int) -> int:
    """
    결제하려는 상품의 배송비를 포함한 총 결제금액을 구하는 service
    Args:
        product_count (int): 유저가 고른 상품의 수량,
        product_id (int): 유저가 고른 상품의 id

    Returns:
        int: (상품의 금액 * 상품의 수량) + 배송비
    """
    product_obj = ProductModel.objects.get(id=product_id)
    total_price = int(product_count) * int(product_obj.price) + \
        int(product_obj.delivery_fee)
    return total_price


def check_user_can_pay(total_price: int, user: User) -> bool:
    """
    유저가 결제할 수 있는 포인트를 지녔는가를 확인하는 service
    Args:
        total_price (int): 유저가 결제를 해야하는 포인트
        user (User): 로그인이 되어있는 user_obj

    Returns:
        bool: 결제할 포인트가 있다면 True
              결제할 포인트가 없다면 False
    """
    if user.point >= total_price:
        return True
    return False


def pay_user_point(total_price: int, user: User) -> int:
    """
    결제 직전 유저의 포인트가 차감이 되는 servic
    Args:
        total_price (int): 결제해야하는 총 금액
        user (User): 로그인이 되어있는 User_obj

    Returns:
        int: 결제가 이루어진 후 남아있는 유저의 포인트
    """
    user.point = int(user.point) - int(total_price)
    user.save()
    return user.point


def create_pay_history(pay_data: dict, user: User, product_id: int, balance_point: int, total_price: int) -> None:
    """
    결제가 진행된 후, 결제내역을 생성해주는 Service
    Args:
        pay_data (dict): {
            count (int) : 결제할 상품의 수량
        }
        user (User): 로그인한 user_obj,
        product_id (int): 결제하려는 상품의 id,
        balance_point (int): 결제하고 난 뒤의 잔액 포인트
        total_price (int): 결제하려는 총 금액
    """
    pay_data["user"] = user.id
    pay_data["product"] = product_id
    pay_data["balance"] = balance_point
    pay_data["total_price"] = total_price
    pay_history_serializer = PayHistorySerializer(data=pay_data)
    pay_history_serializer.is_valid(raise_exception=True)
    pay_history_serializer.save()


def read_pay_history() -> PayHistorySerializer:
    """
    전체 결제내역을 확인하는 service
    Returns:
        PayHistorySerializer: 결제내역 전체의 seriliazer
    """
    all_pay_history = PayHistoryModel.objects.all()
    pay_history_serializer = PayHistorySerializer(
        all_pay_history, many=True).data
    return pay_history_serializer


def detail_read_pay_history(pay_history_id: int) -> PayHistorySerializer:
    """
    결제내역 하나의 상세내역을 확인하는 service
    Args:
        pay_history_id (int): 상세확인할 결제내역의 id
    Returns:
        PayHistorySerializer: 상세확인할 결제내역의 serilizer
    """
    pay_history_obj = PayHistoryModel.objects.get(id=pay_history_id)
    detail_pay_history_serializer = PayHistorySerializer(pay_history_obj).data
    return detail_pay_history_serializer


def refund_product(pay_history_id: int):
    """
    결제내역을 토대로 환불을 진행하는 service
    Args:
        pay_history_id (int): _description_
    """
    pay_history_obj = PayHistoryModel.objects.get(id=pay_history_id)
    user = pay_history_obj.user
    user.point = int(user.point) + int(pay_history_obj.total_price)
    pay_history_obj.delete()
    user.save()

    return pay_history_obj.total_price, user.point
