import django_filters
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models.product import Product
from .models.category import Category
from .models.brand import Brand
from .models.product_other import ProductVariant


class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="search_filter", label="Поиск")
    min_price = django_filters.NumberFilter(
        field_name="variants__price", lookup_expr="gte", label="Мин. цена"
    )
    max_price = django_filters.NumberFilter(
        field_name="variants__price", lookup_expr="lte", label="Макс. цена"
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), field_name="category", label="Категория"
    )
    brand = django_filters.ModelChoiceFilter(
        queryset=Brand.objects.all(), field_name="brand", label="Бренд"
    )
    color = django_filters.CharFilter(field_name="variants__color", label="Цвет")
    size = django_filters.CharFilter(field_name="variants__size", label="Размер")
    min_discount = django_filters.NumberFilter(
        field_name="variants__discount", lookup_expr="gte", label="Мин. скидка"
    )
    max_discount = django_filters.NumberFilter(
        field_name="variants__discount", lookup_expr="lte", label="Макс. скидка"
    )
    date_from = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gte", label="С даты"
    )
    date_to = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lte", label="До даты"
    )

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "category",
            "brand",
            "min_price",
            "max_price",
            "search",
            "color",
            "size",
            "min_discount",
            "max_discount",
            "date_from",
            "date_to",
        ]

    def search_filter(self, queryset, name, value):
        vector = SearchVector("title", "description")
        query = SearchQuery(value)
        return (
            Product.objects.annotate(rank=SearchRank(vector, query))
            .filter(rank__gt=0)
            .order_by("-rank")
        )


class ProductVariantFilter(django_filters.FilterSet):
    color = django_filters.CharFilter(field_name="color", lookup_expr="iexact")
    size = django_filters.CharFilter(field_name="size", lookup_expr="iexact")

    class Meta:
        model = ProductVariant
        fields = ["color", "size"]
