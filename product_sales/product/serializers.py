
from rest_framework import serializers
from .models import Product as ProductModel, PayHistory as PayHistoryModel

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = "__all__"

class PayHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PayHistoryModel
        fields = "__all__"

