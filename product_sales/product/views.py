from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .services.product_service import (
    read_product,
    create_product,
    update_product,
    delete_product,
    check_is_admin,
    get_total_price,
    check_user_can_pay,
    pay_user_point,
    create_pay_history,
)

class ProductView(APIView):
    """
    상품에 관련된 View
    """
    def get(self, request):
        read_product_serializer = read_product()
        return Response(read_product_serializer, status=status.HTTP_200_OK)

    def post(self, request):
        if check_is_admin(request.user):
            create_product(request.data, request.user)
            return Response({"detail" : "상품을 등록하였습니다."}, status=status.HTTP_200_OK)
        return Response({"detail" : "관리자만 상품을 등록할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        if check_is_admin(request.user):
            update_product(request.data, product_id)
            return Response({"detail" : "상품을 수정하였습니다."}, status=status.HTTP_200_OK)
        return Response({"detail" : "관리자만 상품을 수정할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        if check_is_admin(request.user):
            delete_product(product_id)
            return Response({"detail" : "상품을 삭제하였습니다."}, status=status.HTTP_200_OK)
        return Response({"detail" : "관리자만 상품을 삭제할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

class PayView(APIView):
    """
    결제에 관련된 View
    """


    def post(self, request, product_id):
        user = request.user
        total_price = get_total_price(request.data, product_id)
        if check_user_can_pay(total_price, user):
            balance_point = pay_user_point(total_price, user)
            create_pay_history(request.data, user, product_id ,balance_point, total_price)
            return Response({"detail" : ("결제가 완료되었습니다. 남은 포인트는 " + str(balance_point) + "입니다.")}, status=status.HTTP_200_OK)
        return Response({"detail" : "포인트가 부족합니다."}, status=status.HTTP_400_BAD_REQUEST)

    