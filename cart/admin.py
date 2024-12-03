from django.contrib import admin
from .models import Cart


class CartTabAdmin(admin.TabularInline):  # Связь между корзиной и продуктами в админке
    model = Cart  # Модель для связи между корзиной и продуктами
    #  Поля, которые будут отображаться в админке
    fields = ("product_variant", "quantity", "created_timestamp")
    #  Поиск по названию продукта, количество и дате создания
    search_fields = ("product_variant", "quantity", "created_timestamp")
    #  Поля, которые нельзя будет редактировать в админке
    readonly_fields = ("created_timestamp",)
    #  Количество дополнительных пустых форм
    extra = 1


@admin.register(Cart)  # Регистрация модели Cart в админ-панели
class CartAdmin(admin.ModelAdmin):  # Класс админки для модели Cart
    # Поля, которые будут отображаться в админке
    list_display = ("user_display", "product_variant", "quantity", "created_timestamp")
    # Фильтры в списке продуктов
    list_filter = ("created_timestamp", "product_variant__product__title", "user")

    def user_display(self, obj):  # Метод для отображения пользователя в админке
        if obj.user:
            return str(obj.user.username)
        return "Анонимный пользователь"
