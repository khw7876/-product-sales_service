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
    read_pay_history,
    detail_read_pay_history,
    refund_product
)

class ProductView(APIView):
    """
    상품에 관련된 View
    """
    def get(self, request):
        """
        (Read) 모든 저장된 상품을 확인하는 메소드
        """
        read_product_serializer = read_product()
        return Response(read_product_serializer, status=status.HTTP_200_OK)

    def post(self, request):
        """
        (Create) 관리자가 새로운 상품을 등록하는 메소드
        """
        if check_is_admin(request.user):
            create_product(request.data, request.user)
            return Response({"detail" : "상품을 등록하였습니다."}, status=status.HTTP_200_OK)
        return Response({"detail" : "관리자만 상품을 등록할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        """
        (Update) 관리자가 등록된 상품을 수정하는 메소드
        """
        if check_is_admin(request.user):
            update_product(request.data, product_id)
            return Response({"detail" : "상품을 수정하였습니다."}, status=status.HTTP_200_OK)
        return Response({"detail" : "관리자만 상품을 수정할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        """
        (Delete) 관리자가 등록된 상품을 삭제하는 메소드
        """
        if check_is_admin(request.user):
            delete_product(product_id)
            return Response({"detail" : "상품을 삭제하였습니다."}, status=status.HTTP_200_OK)
        return Response({"detail" : "관리자만 상품을 삭제할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

class PayView(APIView):
    """
    사용자의 상품결제에 관련된 View
    """
    def get(self, request):
        """
        (Read) 모든 상품결제의 로그를 확인하는 메소드
        """
        pay_history_serializer = read_pay_history()
        return Response(pay_history_serializer, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        """
        (Create) 유저가 상품을 결제하는 메소드
        """
        user = request.user
        total_price = get_total_price(request.data["count"], product_id)
        if check_user_can_pay(total_price, user):
            balance_point = pay_user_point(total_price, user)
            create_pay_history(request.data, user, product_id ,balance_point, total_price)
            return Response({"detail" : ("결제가 완료되었습니다. 남은 포인트는 " + str(balance_point) + "입니다.")}, status=status.HTTP_200_OK)
        return Response({"detail" : "포인트가 부족합니다."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pay_history_id):
        """
        (Delete) 유저가 구매한 상품을 환불하는 메소드
        """
        if check_is_admin(request.user):
            refund_price, after_user_point = refund_product(pay_history_id)
            return Response({"detail" : ("환불이 완료되었습니다. " + str(refund_price) + "포인트가 환불되어서 현재 포인트는" + str(after_user_point) + "입니다.")}, status=status.HTTP_200_OK)
        return Response({"detail" : "관리자만 환불을 진행 할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)


class DetailPayHistoryView(APIView):
    """
    결제 상세내역 조회
    """
    def get(self, request, pay_history_id):
        """
        (Read) 결제내역의 ID를가지고 상세 내역을 확인하는 메소드
        """
        detail_pay_history_serializer = detail_read_pay_history(pay_history_id)
        return Response(detail_pay_history_serializer, status=status.HTTP_200_OK)

