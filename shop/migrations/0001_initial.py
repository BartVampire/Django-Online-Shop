# Generated by Django 5.1.1 on 2024-09-25 17:26

import django.db.models.deletion
import shop.models.product_other
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Бренд"),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name="Название ссылки",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="products_images/brands/",
                        verbose_name="Изображение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Бренд",
                "verbose_name_plural": "Бренды",
            },
        ),
        migrations.CreateModel(
            name="Characteristic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "Характеристика",
                "verbose_name_plural": "Характеристики",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, verbose_name="Название"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=255, unique=True, verbose_name="Название ссылки"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="products_images/category",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="shop.category",
                        verbose_name="Родительская категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "unique_together": {("slug", "parent")},
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "slug",
                    models.SlugField(
                        max_length=255, unique=True, verbose_name="Название ссылки"
                    ),
                ),
                (
                    "available",
                    models.BooleanField(default=True, verbose_name="Наличие"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        max_length=150,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="shop.brand",
                        verbose_name="Бренд",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="products",
                        to="shop.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты",
            },
        ),
        migrations.CreateModel(
            name="ProductProxy",
            fields=[],
            options={
                "verbose_name": "Продукт прокси",
                "verbose_name_plural": "Продукты прокси",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("shop.product",),
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=shop.models.product_other.product_image_path,
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "is_main",
                    models.BooleanField(
                        default=False, verbose_name="Главное изображение"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="shop.product",
                        verbose_name="Продукт",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение продукта",
                "verbose_name_plural": "Изображения продукта",
            },
        ),
        migrations.CreateModel(
            name="ProductCharacteristic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=255, verbose_name="Значение")),
                (
                    "characteristic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.characteristic",
                        verbose_name="Характеристика",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="characteristics",
                        to="shop.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Характеристика продукта",
                "verbose_name_plural": "Характеристики продукта",
                "unique_together": {("product", "characteristic")},
            },
        ),
        migrations.CreateModel(
            name="ProductVariant",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("size", models.CharField(max_length=50, verbose_name="Размер")),
                ("color", models.CharField(max_length=50, verbose_name="Цвет")),
                (
                    "stock",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Количество на складе"
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Цена",
                    ),
                ),
                (
                    "discount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=4,
                        verbose_name="Скидка в %",
                    ),
                ),
                (
                    "article",
                    models.CharField(
                        blank=True, max_length=13, unique=True, verbose_name="Артикул"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variants",
                        to="shop.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Вариант продукта",
                "verbose_name_plural": "Варианты продукта",
                "indexes": [
                    models.Index(
                        fields=["article"], name="shop_produc_article_83d074_idx"
                    )
                ],
                "unique_together": {("product", "size", "color")},
            },
        ),
    ]