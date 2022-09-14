
from rest_framework import serializers
from .models import User as UserModel

class UserSignupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        condition = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])
        if len(data["username"]) < 4:
            raise serializers.ValidationError("아이디는 4자 이상 입력해주세요.")
        elif UserModel.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("중복된 username이 존재합니다.")
        elif len(data["password"]) < 8 or condition:
            raise serializers.ValidationError("비밀번호는 8자 이상 특수문자 포함해 입력해주세요")
        return data

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user
    
    class Meta:
        model = UserModel
        fields = "__all__"


class UserUpdateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        condition = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])
        if len(data["password"]) < 8 or condition:
            raise serializers.ValidationError("비밀번호는 8자 이상 특수문자 포함해 입력해주세요")
        return data
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = UserModel
        fields = "__all__"
        extra_kwargs = {
            'username': {'read_only': True},
            'point': {'read_only': True},
        }