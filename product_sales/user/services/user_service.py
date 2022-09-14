from django.contrib.auth.hashers import check_password
from user.serializers import UserSignupSerializer, UserUpdateSerializer
from user.models import User as UserModel

def create_user(create_data : dict[str,str]) -> None:
    """
    Args:
        create_data (dict[str,str]): views.py에서 넘겨준 request.data{
            "username" (str): user의 username,
            "password: (str): user의 password
        }
    """
    create_data["point"] = 0
    user_data_serializer = UserSignupSerializer(data=create_data)
    user_data_serializer.is_valid(raise_exception=True)
    user_data_serializer.save()

def update_user(update_data : dict[str, str], user: UserModel) -> None:
    user_data_serializer = UserUpdateSerializer(user, data=update_data, partial=True)
    user_data_serializer.is_valid(raise_exception=True)
    user_data_serializer.save()

def delete_user(user_id):
    user_for_delete = UserModel.objects.get(id=user_id)
    user_for_delete.is_active = False

def check_password_is_possible(password, user):
    if (check_password(password, user.password)):
        return False
    return True