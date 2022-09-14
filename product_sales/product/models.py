from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField("상품이름", max_length=40)
    price = models.IntegerField("상품가격")
    delivery_fee = models.IntegerField("배송비")

    def __str__(self):
        return self.name