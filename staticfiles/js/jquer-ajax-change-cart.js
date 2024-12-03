$(document).ready(function() {
    var isProcessing = false;

    // Функция для обновления цены
    function updateProductPrice($input) {
        var pricePerUnit = parseFloat($input.closest('tr').find('.money-js').data('price'));
        var quantity = parseInt($input.val());
        var totalPrice = (pricePerUnit * quantity).toFixed(2);

        // Обновляем отображаемую цену
        $input.closest('tr').find('.money-js').text(totalPrice);
    }

    // Обработчик события для уменьшения значения
    $(document).off("click", ".qtyBtn.minus").on("click", ".qtyBtn.minus", function (e) {
        e.preventDefault();
        if (isProcessing) return;
        isProcessing = true;

        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.qtyField').find('input[type="number"]');
        var currentValue = parseInt($input.val());

        if (currentValue > 1) {
            $input.val(currentValue - 1);
            updateProductPrice($input); // обновляем цену на клиенте
            updateCart(cartID, currentValue - 1, -1, url, $input);
        } else {
            isProcessing = false;
        }
    });

    // Обработчик события для увеличения значения
    $(document).off("click", ".qtyBtn.plus").on("click", ".qtyBtn.plus", function (e) {
        e.preventDefault();
        if (isProcessing) return;
        isProcessing = true;

        var url = $(this).data("cart-change-url");
        var cartID = $(this).data("cart-id");
        var $input = $(this).closest('.qtyField').find('input[type="number"]');
        var currentValue = parseInt($input.val());

        // Получаем доступное количество товара на складе
        var availableStock = parseInt($input.data("available-stock"), 10);
        console.log('Доступное количество на складе:', availableStock);

         // Проверяем, что увеличенное количество не превышает доступное на складе
        if (currentValue + 1 > availableStock) {
            alert("Вы не можете заказать больше, чем доступно на складе.");
            isProcessing = false;  // Отключаем флаг обработки
            return;
        }

        $input.val(currentValue + 1);
        updateProductPrice($input); // обновляем цену на клиенте
        updateCart(cartID, currentValue + 1, 1, url, $input);
    });


    // Функция для обновления корзины
    function updateCart(cartID, quantity, change, url, $input) {
        $.ajax({
            type: "POST",
            url: url,
            headers: {
                'X-CSRFToken': $("[name=csrfmiddlewaretoken]").val()
            },
            data: {
                cart_id: cartID,
                quantity: quantity
            },
            success: function (data) {
                // Обновляем общую сумму
                $("#total-quantity").text(data.total_quantity);
                $("#total-price").text(data.total_price);
                $("#total-price-summary").text(data.total_price);
                $("#total-price-all").text(data.total_price);

                isProcessing = false;
            },
            error: function (data) {
                console.log("Ошибка при изменении количества товара в корзине");
                isProcessing = false;
            },
        });
    }
});