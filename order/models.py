from django.core.validators import RegexValidator
from django.db import models

from shop.mixins import IdPrimaryKeyMixin
from shop.models.product_other import ProductVariant

from user.models import User


class OrderItemQuerySet(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(IdPrimaryKeyMixin, models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        default=None,
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    requires_delivery = models.BooleanField(
        default=False, verbose_name="Требуется доставка"
    )
    delivery_address = models.TextField(
        max_length=120, blank=True, null=True, verbose_name="Адрес доставки"
    )
    payment_on_get = models.BooleanField(
        default=False, verbose_name="Оплата при получении"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(
        max_length=50, default="В обработке", verbose_name="Статус заказа"
    )
    comment = models.TextField(
        blank=True, null=True, verbose_name="Комментарий к заказу"
    )
    email = models.EmailField(verbose_name="Электронная почта", blank=True, null=True)

    # Проверка номера телефона с помощью регулярного выражения
    phone_regex = RegexValidator(
        regex=r"^(\+7|7|8)?9\d{9}$",
        message="Номер телефона должен быть в формате: '+79XXXXXXXXX' или '89XXXXXXXXX'.",
    )
    # Поле для ввода номера телефона
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=False,
        null=False,
        verbose_name="Номер телефона",
    )

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_timestamp"]

    def __str__(self):
        if self.user:
            return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name} | Статус {self.status}"
        return f"Заказ № {self.pk} | Анонимный покупатель | Статус {self.status}"

    def clean(self):
        if self.phone_number:  # Если поле не пустое
            normalized_number = self.normalize_phone_number(self.phone_number)
            self.phone_number = "+7" + normalized_number[-10:]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @staticmethod
    def normalize_phone_number(phone):
        phone = "".join(char for char in phone if char.isdigit())
        if len(phone) == 10 and phone.startswith("9"):
            return "7" + phone
        elif len(phone) == 11 and phone.startswith("8"):
            return "7" + phone[1:]
        return phone


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product_variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Продукт",
        default=None,
    )
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        db_table = "order_product"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderItemQuerySet.as_manager()

    def products_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"{self.order} | {self.product_variant.product.title} | {self.name} | {self.price} | {self.quantity}"
