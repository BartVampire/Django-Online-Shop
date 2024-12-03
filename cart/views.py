from django.views import View

from .models import Cart
from cart.mixins.CartMixin import CartMixin
from shop.models.product_other import ProductVariant
from django.http import HttpResponse, JsonResponse


class CartAddView(CartMixin, View):  # Класс для добавления продукта в корзину

    def post(self, request):  # Метод для добавления продукта в корзину
        article = request.POST.get(
            "article"
        )  # Запрашиваем идентификатор продукта из POST-запроса

        quantity = int(request.POST.get("quantity", 1))  # Количество из POST-запроса
        print(f"Количество: {quantity}")
        # Ищем вариант продукта по артикулу
        product_variant = ProductVariant.objects.get(article=article)

        # Проверяем, есть ли достаточно товара на складе
        if quantity > product_variant.stock:
            return JsonResponse({"error": "Недостаточно товара на складе."}, status=400)

        # Ищем корзину по варианту продукта
        cart = self.get_cart(request, product_variant=product_variant)

        # Вывод отладочной информации
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        if cart:
            if cart.quantity + quantity > product_variant.stock:
                return JsonResponse(
                    {"error": "Недостаточно товара на складе"}, status=400
                )
            cart.quantity += 1
            cart.save()
        else:
            # Если корзины не существует, то создаем ее (если пользователь авторизован, то создаем корзину пользователя,
            # если не авторизован, то создаем корзину сессии)
            Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=(
                    request.session.session_key
                    if not request.user.is_authenticated
                    else None
                ),
                product_variant=product_variant,
                quantity=1,
            )
        user_cart = self.get_cart_queryset(request)
        total_quantity = (
            user_cart.total_quantity()
            if callable(user_cart.total_quantity)
            else user_cart.total_quantity
        )
        total_price = (
            user_cart.total_price()
            if callable(user_cart.total_price)
            else user_cart.total_price
        )

        # Отправляем ответ с данными о добавлении в корзину
        response_data = {
            "cart_items_html": self.render_cart_add(request),
            "total_quantity": total_quantity,  # Количество продуктов в корзине
            "total_price": total_price,  # Сумма всех продуктов в корзине
        }

        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get(
            "cart_id"
        )  # Запрашиваем идентификатор корзины из POST-запроса
        cart = self.get_cart(request, cart_id=cart_id)  # Ищем корзину по идентификатору
        cart.quantity = request.POST.get(
            "quantity"
        )  # Запрашиваем новое количество из POST-запроса
        cart.save()  # Сохраняем изменения в базе данных
        user_cart = self.get_cart_queryset(request)
        # Предполагая, что user_cart.total_quantity и user_cart.total_price возвращают вычисляемые значения
        total_quantity = (
            user_cart.total_quantity()
            if callable(user_cart.total_quantity)
            else user_cart.total_quantity
        )
        total_price = (
            user_cart.total_price()
            if callable(user_cart.total_price)
            else user_cart.total_price
        )

        response_data = {
            "include_cart_html": self.render_cart_change(request)[0],
            "user_cart_html": self.render_cart_change(request)[1],
            "total_quantity": total_quantity,
            "total_price": total_price,
        }
        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get(
            "cart_id"
        )  # Запрашиваем идентификатор корзины из POST-запроса
        cart = self.get_cart(request, cart_id=cart_id)  # Ищем корзину по идентификатору
        quantity = cart.quantity
        cart.delete()  # Удаляем объект корзины из базы данных
        user_cart = self.get_cart_queryset(request)
        # Предполагая, что user_cart.total_quantity и user_cart.total_price возвращают вычисляемые значения
        total_quantity = (
            user_cart.total_quantity()
            if callable(user_cart.total_quantity)
            else user_cart.total_quantity
        )
        total_price = (
            user_cart.total_price()
            if callable(user_cart.total_price)
            else user_cart.total_price
        )
        response_data = {
            "include_cart_html": self.render_cart_change(request)[0],
            "user_cart_html": self.render_cart_change(request)[1],
            "total_quantity": total_quantity,
            "total_price": total_price,
            "quantity_deleted": quantity,
        }
        return JsonResponse(response_data)
