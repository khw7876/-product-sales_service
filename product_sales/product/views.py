from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .services.product_service import (
    read_product,
    create_product,
    update_product,
    check_is_admin,
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

    