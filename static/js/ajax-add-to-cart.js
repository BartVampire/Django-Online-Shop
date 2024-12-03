// Обработчик для добавления в корзину продукта
$(document).ready(function() {
    $('#add-to-cart-form').on('submit', function(e) {
        e.preventDefault();  // Отключаем стандартную отправку формы

        var $form = $(this);
        var url = $form.data('cart-add-url');  // Получаем URL для добавления в корзину
        var data = $form.serialize();  // Собираем данные формы

         // Получаем доступное количество товара на складе из HTML
        var availableStock = parseInt($form.data('available-stock'), 10);
        var requestedQuantity = parseInt($("[name='quantity']", $form).val(), 10);
        console.log("Количество переданного товара:", requestedQuantity);
        console.log("Количество товара на складе:", availableStock);
        // Проверка количества товара
        if (requestedQuantity > availableStock) {
            alert('Вы пытаетесь заказать больше товара, чем есть на складе.');
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            headers: {
                'X-CSRFToken': $("[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
            // Обновляем содержимое мини-корзины после успешного добавления товара
                $("#header-cart").html(response.cart_items_html);

                   // Обновляем общую сумму и количество товаров в мини-корзине
                $('#total-quantity').text(response.total_quantity);
                $('#total-price').text(response.total_price);

                alert('Товар успешно добавлен в корзину!');
            },
            error: function() {
                alert('Ошибка при добавлении товара в корзину.');
            }
        });
    });
});
