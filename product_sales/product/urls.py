from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductView.as_view(), name="product_view"),
    path("<int:product_id>", views.ProductView.as_view(), name="product_id_view"),
    path("pay_history", views.PayView.as_view(), name="pay_view"),
    path("pay/<int:product_id>", views.PayView.as_view(), name="pay_id_view"),
    path("refund/<int:pay_history_id>", views.PayView.as_view(), name="pay_history_id_view"),
    path("pay_histroy/<int:pay_history_id>", views.DetailPayHistoryView.as_view(), name="detail_pay_history_id_view"),
]
