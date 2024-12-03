from django.contrib import admin

from order.models import OrderItem, Order


class OrderItemTabularAdmin(admin.TabularInline):  # Взаимодействие с моделью OrderItem
    model = OrderItem  # Используемая модель
    fields = (
        "product_variant",
        "name",
        "price",
        "quantity",
    )  # Поля, которые будут отображаться в админке
    search_fields = (
        "product_variant",
        "name",
    )  # Поля, по которым будет осуществляться поиск
    extra = 0  # Количество дополнительных полей


@admin.register(Order)  # Декоратор для регистрации модели в админке
class OrderAdmin(admin.ModelAdmin):  # Класс админки для модели Order
    # Поля, которые будут отображаться в админке
    list_display = (
        "id",
        "user",
        "requires_delivery",
        "status",
        "is_paid",
        "payment_on_get",
        "created_timestamp",
    )
    # Поля, по которым будет осуществляться поиск
    search_fields = ("id", "is_paid", "created_timestamp", "user")
    # Поля, которые будут отображаться в админке в режиме только для чтения
    readonly_fields = ("created_timestamp",)
    # Список полей, по которым можно фильтровать в админке
    list_filter = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
    )
    # Взаимодействие с моделью OrderItem (связь многие-ко-многим)
    inlines = [
        OrderItemTabularAdmin,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product_variant",
        "name",
        "price",
        "quantity",
    )
    search_fields = (
        "order",
        "product_variant",
        "name",
    )


class OrderTabularAdmin(admin.TabularInline):
    model = Order
    fields = (
        "requires_delivery",
        "status",
        "is_paid",
        "payment_on_get",
        "created_timestamp",
    )
    search_fields = (
        "requires_delivery",
        "status",
        "is_paid",
        "payment_on_get",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0
