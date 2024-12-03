from django.urls import path
from order.views import CreateOrderView

app_name = "orders"

urlpatterns = [
    path("create_order/", CreateOrderView.as_view(), name="create_order"),
]
