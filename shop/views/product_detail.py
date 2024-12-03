from django.views.generic import DetailView
from shop.models.product import Product
from shop.models.product_other import (
    ProductVariant,
    ProductImage,
    ProductCharacteristic,
)
from django.shortcuts import get_object_or_404


class ProductDetailView(DetailView):
    """
    Класс для отображения деталей конкретного продукта.
    Использует generic DetailView для отображения одного объекта модели Product.
    """

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product_detail"

    def get_object(self):
        slug = self.kwargs.get("slug")
        article = self.kwargs.get("article")
        return get_object_or_404(Product, slug=slug, variants__article=article)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Получаем выбранные параметры цвета и размера
        selected_color = self.request.GET.get("color")
        selected_size = self.request.GET.get("size")

        # Если выбран цвет, но не выбран размер или размер недоступен для этого цвета, сбрасываем параметр `size`
        variants = ProductVariant.objects.filter(product=product)

        if selected_color:
            # Фильтруем варианты по цвету
            variants = variants.filter(color=selected_color)

            # Проверяем, доступен ли выбранный размер для выбранного цвета
            available_sizes = variants.values_list("size", flat=True).distinct()

            if selected_size not in available_sizes:
                # Если размер не доступен для выбранного цвета, сбрасываем выбранный размер
                selected_size = None

        # Фильтрация по выбранному размеру
        if selected_size:
            variants = variants.filter(size=selected_size)

        # Определяем выбранный вариант
        selected_variant = variants.first() if variants.exists() else None
        print(f"Выбранный вариант: {selected_variant}")
        # Заполняем контекст
        context["main_image_prefetched"] = ProductImage.objects.filter(
            product=product, is_main=True
        )
        context["additional_images"] = ProductImage.objects.filter(
            product=product, is_main=False
        )
        context["characteristics"] = ProductCharacteristic.objects.filter(
            product=product
        )

        # Все доступные цвета для продукта
        context["colors"] = list(
            ProductVariant.objects.filter(product=product)
            .values_list("color", flat=True)
            .distinct()
        )

        # Доступные размеры для выбранного цвета
        if selected_color:
            context["sizes"] = list(
                ProductVariant.objects.filter(product=product, color=selected_color)
                .values_list("size", flat=True)
                .distinct()
            )
        else:
            context["sizes"] = []

        # Если выбранный вариант существует, добавляем его в контекст
        context["selected_variant"] = selected_variant

        return context
