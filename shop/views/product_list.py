from django.core.cache import cache
from django.db.models import Prefetch
from django.http import Http404
from django.views.generic import ListView
from django_filters.views import FilterMixin

from shop.models.brand import Brand
from shop.models.product import ProductProxy
from shop.models.category import Category
from shop.filters import ProductFilter
from shop.models.product_other import ProductCharacteristic, ProductImage


class CategoryProductsListView(FilterMixin, ListView):
    model = ProductProxy
    filterset_class = ProductFilter
    template_name = "products_list.html"
    paginate_by = 12
    context_object_name = "products_list"

    def get_queryset(self):

        # Уникальный ключ для кэширования
        cache_key = "product_list_view_all"

        # Попробуем получить данные из кэша
        queryset = cache.get(cache_key)

        if queryset is None:
            # Загрузка связанных моделей для оптимизации и добавление prefetch для изображений и характеристик
            queryset = (
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
                )
                .order_by("-id")
            )
            # Кэшируем данные
            cache.set(cache_key, queryset, 60 * 20)

        # Получаем slug для категории или бренда
        category_or_brand_slug = self.kwargs.get("slug")
        if category_or_brand_slug:
            # Сначала проверяем, является ли slug брендом
            if Brand.objects.filter(slug=category_or_brand_slug).exists():
                brand = Brand.objects.get(slug=category_or_brand_slug)
                queryset = queryset.filter(brand=brand)
                print(f"Фильтрация по бренду: {brand}, slug={category_or_brand_slug}")
            # Если это не бренд, проверяем категорию
            elif Category.objects.filter(slug=category_or_brand_slug).exists():
                category = Category.objects.get(slug=category_or_brand_slug)
                queryset = queryset.filter(category=category)
                print(
                    f"Фильтрация по категории: {category}, slug={category_or_brand_slug}"
                )
            else:
                # Если ни категория, ни бренд не найдены, выводим 404
                raise Http404(
                    f"No Category or Brand matches the given query: {category_or_brand_slug}"
                )
        else:
            print("Категория или бренд не выбраны")

        # Фильтрация по цене через связанные объекты (ProductVariant)
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            queryset = queryset.filter(variants__price__gte=min_price)
            print(f"Фильтрация по минимальной цене: {min_price}")
        if max_price:
            queryset = queryset.filter(variants__price__lte=max_price)
            print(f"Фильтрация по максимальной цене: {max_price}")

        # Применение других фильтров через FilterSet
        self.filterset = self.get_filterset(queryset=queryset)
        print(f"Финальный queryset после всех фильтров: {self.filterset.qs}")

        return self.filterset.qs

    def get_filterset(self, **kwargs):
        filterset = self.filterset_class(self.request.GET, **kwargs)
        print(f"Созданный фильтр: {filterset}")
        return filterset

    def get_brands(self, queryset):
        # Получение уникальных брендов из отфильтрованного списка продуктов
        brands = (
            queryset.select_related("brand")
            .values_list("brand__slug", "brand__name")
            .distinct()
        )
        print(f"Список брендов для текущего queryset: {list(brands)}")
        return brands

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.get_filterset()

        # Получаем slug категории или бренда
        category_or_brand_slug = self.kwargs.get("slug")
        if category_or_brand_slug:
            # Сначала проверяем, является ли slug брендом
            if Brand.objects.filter(slug=category_or_brand_slug).exists():
                brand = Brand.objects.get(slug=category_or_brand_slug)
                queryset = ProductProxy.objects.filter(brand=brand)
                context["brands"] = self.get_brands(queryset)
                context["current_brand"] = brand
                context["current_category"] = None
                print(f"Текущий бренд: {brand}")
            # Если это не бренд, проверяем категорию
            elif Category.objects.filter(slug=category_or_brand_slug).exists():
                category = Category.objects.get(slug=category_or_brand_slug)
                queryset = ProductProxy.objects.filter(category=category)
                context["brands"] = self.get_brands(queryset)
                context["current_category"] = category
                context["current_brand"] = None
                print(f"Текущая категория: {category}")
            else:
                raise Http404(
                    f"No Category or Brand matches the given query: {category_or_brand_slug}"
                )
        else:
            context["brands"] = self.get_brands(ProductProxy.objects.all())
            context["current_category"] = None
            context["current_brand"] = None
            print("Категория и бренд не выбраны, вывод всех брендов")

        # Передаём выбранные параметры фильтрации в контекст
        context["selected_brands"] = self.request.GET.getlist("brand", [])
        context["selected_min_price"] = self.request.GET.get("min_price", None)
        context["selected_max_price"] = self.request.GET.get("max_price", None)

        print(f"Контекст: {context}")

        return context
