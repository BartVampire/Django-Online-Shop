from django.template.loader import render_to_string
from cart.models import Cart
from cart.utils import get_user_carts


class CartMixin:  # Миксин для работы с корзиной
    def get_cart(self, request, product_variant=None, cart_id=None):
        if request.user.is_authenticated:  # Если пользователь авторизован
            query_kwargs = {"user": request.user}  # Ищем корзину пользователя
        else:  # Если пользователь не авторизован
            query_kwargs = {
                "session_key": request.session.session_key
            }  # Ищем корзину по сессии

        if product_variant:  # Если передан продукт
            query_kwargs["product_variant"] = (
                product_variant  # Ищем корзину по продукту
            )
        if cart_id:  # Если передан id корзины
            query_kwargs["id"] = cart_id  # Ищем корзину по id

        return Cart.objects.filter(**query_kwargs).first()  # Возвращаем корзину

    def render_cart_add(
        self, request
    ):  # Рендеринг добавления в корзину в шаблоне сайта
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}

        return render_to_string(
            "carts/includes/mini_cart.html", context=context, request=request
        )

    def render_cart_change(self, request):
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}
        include_cart_html = render_to_string(
            "carts/includes/mini_cart.html", context=context, request=request
        )
        user_cart_html = render_to_string(
            "carts/includes/cart_page.html", context=context, request=request
        )
        return include_cart_html, user_cart_html

    def get_cart_queryset(self, request):
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        return Cart.objects.filter(**query_kwargs)
