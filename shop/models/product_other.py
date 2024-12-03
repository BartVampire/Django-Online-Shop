from django.db import models
from django.urls import reverse

from .BaseModel import BaseModel
from .product import Product
from ..mixins import IdPrimaryKeyMixin


def product_image_path(
    instance, filename
):  # Путь до изображений продукта в базе данных по slug
    return f"product_images/{instance.product.slug}/{filename}"  # Возвращает путь до изображения продукта


class ProductImage(
    IdPrimaryKeyMixin, models.Model
):  # Модель для хранения изображений продукта
    # Поле product, которое связано с моделью Products
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
    )
    # Поле image, которое связано с моделью ImageField и указывает путь до изображения
    image = models.ImageField(upload_to=product_image_path, verbose_name="Изображение")
    # Поле is_main, которое указывает, является ли изображение главным
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")

    class Meta:  # Мета-описание модели
        verbose_name = "Изображение продукта"  # Название в админке
        verbose_name_plural = "Изображения продукта"  # Название в админке


class Characteristic(models.Model):  # Модель характеристик
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название"
    )  # Название характеристики

    class Meta:  # Мета-описание модели
        verbose_name = "Характеристика"  # Название в админке
        verbose_name_plural = "Характеристики"  # Название в админке

    def __str__(self):  # Выводит название характеристики
        return self.name  # Возвращает название характеристики


class ProductCharacteristic(BaseModel, models.Model):  # Модель характеристик продукта
    # Поле product, которое связано с моделью Products
    product = models.ForeignKey(
        Product, related_name="characteristics", on_delete=models.CASCADE
    )
    # Поле characteristic, которое связано с моделью Characteristic и указывает название характеристики
    characteristic = models.ForeignKey(
        Characteristic, on_delete=models.CASCADE, verbose_name="Характеристика"
    )
    # Поле value, которое указывает значение характеристики продукта
    value = models.CharField(max_length=255, verbose_name="Значение")

    class Meta:  # Мета-описание модели
        verbose_name = "Характеристика продукта"  # Название в админке
        verbose_name_plural = "Характеристики продукта"  # Название в админке
        unique_together = (
            "product",
            "characteristic",
        )  # Уникальные пары продукта и характеристики

    def __str__(self):
        return f"{self.characteristic.name}: {self.value}"  # Выводит название характеристики и значение


class ProductVariant(IdPrimaryKeyMixin, models.Model):
    product = models.ForeignKey(
        Product, related_name="variants", on_delete=models.CASCADE
    )
    size = models.CharField(
        max_length=50, verbose_name="Размер"
    )  # Пример характеристики
    color = models.CharField(
        max_length=50, verbose_name="Цвет"
    )  # Пример характеристики
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена", blank=True, null=True
    )
    discount = models.DecimalField(
        default=0.00, max_digits=4, decimal_places=2, verbose_name="Скидка в %"
    )
    article = models.CharField(
        max_length=13, unique=True, blank=True, verbose_name="Артикул"
    )

    class Meta:
        verbose_name = "Вариант продукта"
        verbose_name_plural = "Варианты продукта"
        unique_together = (
            "product",
            "size",
            "color",
        )  # Уникальный вариант по комбинации характеристик
        indexes = [
            models.Index(fields=["article"]),
        ]  # Добавляем индекс по артикулу и названию для быстрого поиска

    def __str__(self):
        return f"{self.product.title} - Цвет: |{self.color}| - Размер: |{self.size}| - Артикул: {self.article}"

    def save(self, *args, **kwargs):
        self.article = BaseModel.generate_unique_article()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "shop:product_details",
            kwargs={"slug": self.product.slug, "article": self.article},
        )

    def sell_price(self):  # Метод, который возвращает цену с учетом скидки
        if self.discount > 0:
            return round(self.price - (self.price * self.discount / 100), 2)
        else:
            return self.price
