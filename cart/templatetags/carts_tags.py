from django import template
from cart.utils import get_user_carts

register = template.Library()


@register.simple_tag()  # Это декоратор, который регистрирует функцию как простой шаблонный тег Django.
def user_carts(request):  # Функция для получения корзин пользователя
    return get_user_carts(request)  # Возвращаем корзину пользователя
