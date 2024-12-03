from django.contrib import admin

from cart.admin import CartTabAdmin
from user.models import User

# from orders.admin import OrderTabularAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):  # Класс админки для модели User
    # Поля, которые будут отображаться в админке
    list_display = ["username", "email", "first_name", "last_name", "phone_number"]
    # Поиск по названию пользователя, почте, имени и фамилии
    search_fields = ["username", "email", "first_name", "last_name"]
    # Связь между корзиной, заказами и пользователями в админке
    inlines = [
        CartTabAdmin,
    ]
    # OrderTabularAdmin
