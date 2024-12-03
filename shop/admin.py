from django.contrib import admin
from django.utils.html import format_html

from shop.models.product import Product
from shop.models.category import Category
from shop.models.brand import Brand
from .models.product_other import (
    ProductVariant,
    ProductImage,
    ProductCharacteristic,
    Characteristic,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    ordering = ("name",)

    def get_prepopulated_fields(self, request, obj=None):
        """
        Заполняет автоматически slug категории, если он не задан. Если slug уже задан, то сохраняет его без изменений.
        """
        return {
            "slug": ("name",),
        }


class ProductImageInline(admin.TabularInline):  # Связь между продуктами и изображениями
    model = ProductImage  # Модель для связи между продуктами и изображениями
    extra = 1  # Количество дополнительных пустых форм
    fields = [
        "image",
        "is_main",
        "image_preview",
    ]  # Поля, которые будут отображаться в админке
    readonly_fields = [
        "image_preview"
    ]  # Поля, которые будут отображаться только для просмотра

    def image_preview(self, obj):  # Метод для предпросмотра изображения в админке
        if obj.image:  # Если изображение существует
            #  Возвращает HTML-код с изображением с указанием ширины и высоты
            return format_html(f"<img src='{obj.image.url}' width='150', height='150'>")
        #  Если изображения нет, возвращает "Нет изображения"
        return "Нет изображения"


class ProductCharacteristicInline(
    admin.TabularInline
):  # Связь между продуктами и характеристиками
    model = (
        ProductCharacteristic  # Модель для связи между продуктами и характеристиками
    )
    extra = 1  # Количество дополнительных пустых форм
    autocomplete_fields = ["characteristic"]  # Поле для автозаполнения


class ProductVariantInline(admin.TabularInline):  # или admin.StackedInline
    model = ProductVariant
    extra = 1  # Количество пустых форм для добавления вариантов


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline, ProductCharacteristicInline]

    list_display = (
        "title",
        "brand",
        "category",
        "slug",
        "available",
        "created_at",
        "updated_at",
    )
    list_filter = ("available", "created_at", "updated_at")
    ordering = ("title",)
    search_fields = ("title", "article", "brand__name", "category__name")

    def main_image_preview(
        self, obj
    ):  # Метод для предпросмотра главного изображения в админке
        main_image = obj.images.filter(
            is_main=True
        ).first()  # Находит главное изображение продукта по фильтру
        if main_image:  # Если главное изображение существует
            #  Возвращает HTML-код с изображением с указанием ширины и высоты
            return format_html(
                f"<img src='{main_image.image.url}' width='50', height='50'>"
            )
        #  Если главного изображения нет, возвращает "Нет изображения"
        return "Нет изображения"

    main_image_preview.short_description = (
        "Главное изображение"  # Выводит название "Главное изображение"
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {
            "slug": ("title",),
        }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "image")
    ordering = ("name",)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            "slug": ("name",),
        }


@admin.register(Characteristic)  # Регистрация модели Characteristic в админ-панели
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ["name"]  # Отображаемые поля в списке характеристик
    search_fields = ["name"]  # Поиск по названию характеристики


@admin.register(ProductImage)  # Регистрация модели ProductImage в админ-панели
class ProductImageAdmin(admin.ModelAdmin):  # Класс админки для модели ProductImage
    list_display = [
        "product",
        "is_main",
        "image_preview",
    ]  # Отображаемые поля в списке изображений
    list_filter = ["is_main"]  # Фильтр по полю "Главное изображение"
    search_fields = ["product__name"]  # Поиск по названию продукта

    # Метод для предпросмотра изображения
    def image_preview(self, obj):  # Метод для предпросмотра изображения
        if obj.image:  # Если изображение существует
            #  Возвращает HTML-код с изображением с указанием ширины и высоты
            return format_html(f"<img src='{obj.image.url}' width='100', height='100'>")
        #  Если изображения нет, возвращает "Нет изображения"
        return "Нет изображения"

    image_preview.short_description = "Предпросмотр"  # Выводит название "Предпросмотр"


@admin.register(
    ProductCharacteristic
)  # Регистрация модели ProductCharacteristic в админ-панели
class ProductCharacteristicAdmin(
    admin.ModelAdmin
):  # Класс админки для модели ProductCharacteristic

    list_display = [
        "product",
        "characteristic",
        "value",
    ]  # Отображаемые поля в списке характеристик
    list_filter = ["characteristic"]  # Фильтр по полю "Характеристика"
    search_fields = [
        "product__name",
        "characteristic__name",
        "value",
    ]  # Поиск по названию продукта, характеристикам
    autocomplete_fields = [
        "product",
        "characteristic",
    ]  # Автозаполнение полей "Продукт" и "Характеристика"
