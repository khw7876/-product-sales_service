from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .services.product_service import (
    create_product,
)

class ProductView(APIView):
    """
    상품에 관련된 View
    """
    def post(self, request):
        create_product(request.data, request.user)
        return Response({"detail" : "상품을 등록하였습니다."}, status=status.HTTP_200_OK)