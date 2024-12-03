from django import forms
from .models import Order


class CreateOrderForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=100)
    last_name = forms.CharField(label="Фамилия", max_length=100)
    email = forms.EmailField(label="Электронная почта")
    phone_number = forms.CharField(
        label="Телефон", validators=[Order.phone_regex], max_length=15
    )
    delivery_address = forms.CharField(
        label="Адрес доставки",
        required=False,
        widget=forms.TextInput(
            attrs={"id": "id_delivery_address"}
        ),  # Добавляем id для поля
    )
    payment_on_get = forms.ChoiceField(
        label="Способ оплаты",
        choices=[("0", "Оплата картой"), ("1", "Наличными/картой при получении")],
    )
    requires_delivery = forms.ChoiceField(
        label="Нужна доставка", choices=[("0", "Самовывоз"), ("1", "Нужна доставка")]
    )

    comment = forms.CharField(label="Комментарий к заказу", required=False)
