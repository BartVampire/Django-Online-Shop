from django.urls import reverse

from shop.models.BaseModel import BaseModel
from django.db import models

from .brand import Brand
from .category import Category
from shop.mixins import IdPrimaryKeyMixin


class Product(IdPrimaryKeyMixin, BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, max_length=150, verbose_name="Бренд"
    )
    description = models.TextField(verbose_name="Описание", blank=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        editable=True,
        verbose_name="Название ссылки",
    )
    # quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    available = models.BooleanField(default=True, verbose_name="Наличие")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        """
        Класс для метаданных модели Product
        """

        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        first_variant = self.variants.first()
        if first_variant:
            return reverse(
                "shop:product_details",
                kwargs={"slug": self.slug, "article": first_variant.article},
            )
        else:
            return reverse("shop:product_details", kwargs={"slug": self.slug})

    def main_image(self):  # Метод, который возвращает главное изображение
        if hasattr(self, "main_image_prefetched"):
            return self.main_image_prefetched[0] if self.main_image_prefetched else None
        return self.images.filter(is_main=True).first()

    def additional_images(
        self,
    ):  # Метод, который возвращает дополнительные изображения
        return self.images.filter(is_main=False)

    def get_characteristics(
        self,
    ):  # Метод, который возвращает характеристики продукта
        return self.characteristics.all()


class ProductManager(models.Manager):
    """
    Класс для управления моделью Product с помощью Manager
    """

    def get_queryset(self):
        """
        Возвращает queryset с отфильтрованными продуктами (только те, где available=True)
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    """
    Класс для проксирования модели Product (для отображения только доступных продуктов)
    """

    objects = ProductManager()

    class Meta:
        proxy = True
        verbose_name = "Продукт прокси"
        verbose_name_plural = "Продукты прокси"
