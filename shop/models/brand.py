from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .BaseModel import BaseModel
from ..mixins import IdPrimaryKeyMixin


class Brand(IdPrimaryKeyMixin, BaseModel):  # Модель бренда
    # Генерация id для модели Brand с помощью mixin IdPrimaryKeyMixin (UUID-генератор)
    # Название бренда (максимальная длина 100 символов, уникальное поле)
    name = models.CharField(max_length=100, unique=True, verbose_name="Бренд")
    # Название бренда (максимальная длина 150 символов, уникальное поле, необязательное поле)
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Название ссылки",
    )
    # Изображение бренда (необязательное поле, загружается в папку products_images/brands/)
    image = models.ImageField(
        upload_to="products_images/brands/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )

    def __str__(self):
        return self.name  # Выводит название бренда

    class Meta:
        verbose_name = "Бренд"  # Название в админке
        verbose_name_plural = "Бренды"  # Название в админке во множественном числе

    def save(
        self,
        *args,
        **kwargs,
    ):
        """
        Сохраняет slug категории, если он не задан. Если slug уже задан, то сохраняет его без изменений.
        """
        if not self.slug:
            self.slug = slugify(BaseModel.random_slug() + "-pickBetter" + self.name)
        super(Brand, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category_products", kwargs={"slug": self.slug})
