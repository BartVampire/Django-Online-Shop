from django.core.cache import cache
from django.http import QueryDict
from shop.models.category import Category
from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg


@register.simple_tag()
def tag_get_categories_with_subcategories():
    # Попробуем получить категории из кэша
    cache_key = "categories_with_subcategories"
    categories = cache.get(cache_key)
    # Если кэша нет, получаем данные из базы и кэшируем их
    if categories is None:
        categories = Category.objects.filter(parent=None).prefetch_related("children")
        for category in categories:
            category.subcategories = category.children.all()

        # Сохраняем результат в кэше на 1 час (3600 секунд)
        cache.set(cache_key, categories, 3600)
    return categories


# @register.simple_tag()  # Это декоратор, который регистрирует функцию как простой шаблонный тег Django.
# def tag_brands():  # Шаблонный тег для получения списка брендов.
#     return Brand.objects.all()  # Возвращаем список брендов.@register.simple_tag()


# @register.simple_tag()  # Это декоратор, который регистрирует функцию как простой шаблонный тег Django.
# def tag_latest_product():  # Шаблонный тег для получения списка брендов.
#     return Products.objects.prefetch_related('cr').order_by('-created_at')

# @register.simple_tag()  # Это декоратор, который регистрирует функцию как простой шаблонный тег Django.
# def query_transform(request, **kwargs):  # Принимает объект request и произвольное количество именованных аргументов(kw)
#     updated = request.GET.copy()  # Создает копию QueryDict, чтобы не изменить оригинальный объект.
#     for k, v in kwargs.items():  # Итерация по всем переданным именованным аргументам.
#         updated[k] = v  # Обновляет или добавляет новые параметры в копию QueryDict.
#     return updated.urlencode()  # Преобразует обновленный QueryDict в URL-encoded строку.
