from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductView.as_view(), name="product_view"),
    path("<int:product_id>", views.ProductView.as_view(), name="product_id_view"),
]
