from django.core.cache import cache
from django.db.models import Prefetch
from django.views.generic import TemplateView
from shop.models.product_other import (
    ProductImage,
    ProductCharacteristic,
    ProductVariant,
)
from shop.models.product import Product, ProductProxy


class MainPageView(TemplateView):
    """
    Класс для отображения главной страницы сайта.
    Использует generic TemplateView для отображения шаблона index.html.
    """

    template_name = "index.html"  # Путь к шаблону

    def get_context_data(
        self, **kwargs
    ):  # Метод, который возвращает контекст для шаблона (index.html)
        context = super().get_context_data(
            **kwargs
        )  # Вызываем родительский метод для получения контекста

        # Уникальный ключ для кэширования
        cache_key = "new_products_queryset_main"

        # Попробуем получить данные из кэша
        new_products_queryset = cache.get(cache_key)

        # Если кэша нет, получаем данные из базы и кэшируем их
        if new_products_queryset is None:
            new_products_queryset = (
                ProductProxy.objects.select_related("category", "brand")
                .prefetch_related(
                    # Префетч для главного изображения
                    Prefetch(
                        "images",
                        queryset=ProductImage.objects.filter(is_main=True),
                        to_attr="main_image_prefetched",
                    ),
                    # Префетч для характеристик продукта
                    Prefetch(
                        "characteristics",
                        queryset=ProductCharacteristic.objects.select_related(
                            "characteristic"
                        ),
                        to_attr="product_characteristics_prefetched",
                    ),
                    # Префетч для дополнительных изображений
                    Prefetch(
                        "images",
                        queryset=ProductImage.objects.filter(is_main=False),
                        to_attr="additional_images_prefetched",
                    ),
                    Prefetch(
                        "variants",
                        queryset=ProductVariant.objects.all(),
                        to_attr="product_variants_prefetched",
                    ),
                )
                .order_by("-id")[:6]
            )  # Получаем новые товары сортированные по дате создания

            # Кэшируем данные
            cache.set(cache_key, new_products_queryset, 60 * 20)

        context["new_products"] = new_products_queryset
        return context  # Возвращаем контекст
