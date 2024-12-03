from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from shop.models.BaseModel import BaseModel
from shop.mixins import IdPrimaryKeyMixin


class Category(IdPrimaryKeyMixin, BaseModel):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        editable=True,
        verbose_name="Название ссылки",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        verbose_name="Родительская категория",
    )
    image = models.ImageField(
        upload_to="products_images/category",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )

    class Meta:
        unique_together = ["slug", "parent"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """
        Возвращает строковое представление категории (название -> родительская категория).
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return " -> ".join(full_path[::-1])

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
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к конкретной категории.
        """

        return reverse("shop:category_products", kwargs={"slug": self.slug})
