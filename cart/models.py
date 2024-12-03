from django.db import models

from shop.mixins import IdPrimaryKeyMixin
from shop.models.BaseModel import BaseModel
from shop.models.product_other import ProductVariant
from shop.models.product import Product
from user.models import User


class CartQuerySet(
    models.QuerySet
):  # Класс для управления моделью Cart с помощью Manager

    def total_price(self):  # Сумма всех продуктов в корзине
        return sum(
            cart.products_price() for cart in self
        )  # Возвращаем сумму цен всех продуктов

    def total_quantity(self):  # Количество продуктов в корзине
        if self:  # Если корзина не пустая
            return sum(
                cart.quantity for cart in self
            )  # Возвращаем сумму количества всех продуктов
        return 0  # Иначе возвращаем ноль


class Cart(IdPrimaryKeyMixin, models.Model):  # Класс для работы с корзиной

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
    )
    product_variant = models.ForeignKey(
        to=ProductVariant, on_delete=models.CASCADE, verbose_name="Вариант продукта"
    )  # Связываем корзину с вариантом продукта
    # Количество
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    session_key = models.CharField(
        max_length=32, blank=True, null=True, verbose_name="Ключ сессии"
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        db_table = "cart"  # Имя таблицы
        verbose_name = "Корзину"  # Название модели
        verbose_name_plural = "Корзины"  # Название модели во множественном числе

    objects = (
        CartQuerySet.as_manager()
    )  # Класс для управления моделью Cart с помощью Manager

    def products_price(self):
        # Вычисляем стоимость продукта с учётом количества и скидки (sell_price)
        return round(self.product_variant.sell_price() * self.quantity, 2)

    def __str__(self):
        if self.user:  # Если пользователь авторизован
            # Возвращаем имя пользователя и название продукта и количество в корзине
            return f"Корзина {self.user.username} | Продукт {self.product_variant.product.title} | Количество {self.quantity}"
        # Если пользователь не авторизован, возвращаем название продукта и количество в корзине
        return f"Анонимная корзина | Продукт {self.product_variant.product.title} | Количество {self.quantity}"
