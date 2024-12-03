from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from cart.models import Cart
from order.forms import CreateOrderForm
from order.models import Order, OrderItem
from django.forms import ValidationError
from django.db import transaction
from user.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "order/checkout.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("users:profile_page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO Убрать приватный API ключ
        context["api_key"] = "231f6605036feee31c6108c8e4f10b8356f65bcd"
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        initial["email"] = self.request.user.email
        initial["phone_number"] = self.request.user.phone_number
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():  # Транзакция для сохранения данных в базе данных в случае ошибки выполнения транзакции произойдет отмена всех изменений
                user = self.request.user  # Получаем самого пользователя
                cart_items = Cart.objects.filter(
                    user=user
                )  # Получаем все корзины пользователя
                if cart_items.exists():  # Если есть хотя бы одна корзина
                    # Создаем заказ пользователя
                    order = Order.objects.create(
                        user=user,
                        requires_delivery=form.cleaned_data["requires_delivery"],
                        delivery_address=form.cleaned_data["delivery_address"],
                        payment_on_get=form.cleaned_data["payment_on_get"],
                        email=form.cleaned_data["email"],
                        phone_number=form.cleaned_data["phone_number"],
                        comment=form.cleaned_data["comment"],
                    )
                    for cart_item in cart_items:  # Перебираем все корзины пользователя
                        product = (
                            cart_item.product_variant
                        )  # Перебираем все продукты в корзине пользователя
                        name = (
                            cart_item.product_variant.product.title
                        )  # Перебираем все названия в корзине пользователя
                        price = (
                            cart_item.product_variant.sell_price()
                        )  # Перебираем все цены в корзине пользователя
                        quantity = (
                            cart_item.quantity
                        )  # Перебираем все количества в корзине пользователя

                        if (
                            product.stock < quantity
                        ):  # Если количество продукта меньше количества в корзине
                            raise ValidationError(
                                f"Недостаточное количество товара {name} на складе\
                                                            В наличии {product.stock} шт."
                            )
                        OrderItem.objects.create(
                            order=order,
                            product_variant=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        product.stock -= quantity
                        product.save()
                    cart_items.delete()

                    messages.success(self.request, "Заказ успешно оформлен!")
                    return redirect("user:profile_page")

        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect("order:create_order")

    def form_invalid(self, form):
        messages.error(self.request, "Заполните все обязательные поля!")
        return redirect("order:create_order")
