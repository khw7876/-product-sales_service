from itertools import count
from django.db import models
from user.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField("상품이름", max_length=40)
    price = models.IntegerField("상품가격")
    delivery_fee = models.IntegerField("배송비")

    def __str__(self):
        return self.name


class PayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField("주문 수량")
    balance = models.IntegerField("주문 후 유저의 잔액")
    total_price = models.IntegerField("총 주문 금액")
    create_date = models.DateTimeField("주문 날짜", auto_now_add=True)

    def __str__(self):
        return self.user / self.product
