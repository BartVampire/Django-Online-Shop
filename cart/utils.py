from .models import Cart


def get_user_carts(request):  # Получение корзин пользователя
    if request.user.is_authenticated:  # Если пользователь авторизован
        return Cart.objects.filter(user=request.user).select_related(
            "product_variant", "product_variant__product"
        )  # Ищем корзину пользователя

    if (
        not request.session.session_key
    ):  # Если сессия не создана (пользователь не авторизован)
        request.session.create()  # Создаем сессию
    return Cart.objects.filter(session_key=request.session.session_key).select_related(
        "product_variant"
    )  # Ищем корзину по сессии
