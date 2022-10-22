from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from user.services.user_service import (
    create_user,
    update_user,
    delete_user,
    check_password_is_possible,
    charge_point,
)


class UserView(APIView):
    """
    회원정보 조회 및 회원가입
    """

    def post(self, request: Request) -> Response:
        create_user(request.data)
        return Response({"detail": "회원가입을 성공하였습니다"}, status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        user = request.user
        if check_password_is_possible(request.data["password"], user):
            update_user(request.data, user)
            return Response({"detail": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response({"detail": "기존의 비밀번호와 일치하는 비밀번호입니다."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, user_id: int) -> Response:
        delete_user(user_id)
        return Response({"detail": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)


class ChargePointView(APIView):
    """
    유저가 포인트를 충전하는 View
    """

    def post(self, request):
        user = request.user
        before_point, cur_point = charge_point(request.data, user)
        return Response({"detail": (user.username + "님의 포인트가 " + str(before_point) + "포인트가 충전되어서" + str(cur_point) + "포인트가 되셨습니다.")}, status=status.HTTP_200_OK)
