$(document).ready(function() {
    var isProcessing = false;

    // Обработчик для удаления товара (общий для основной корзины и мини-корзины)
    $(document).on("click", ".cart__remove", function(e) {
        e.preventDefault();
        if (isProcessing) return;
        isProcessing = true;

        var url = $(this).attr("href");  // URL для удаления товара
        var cartID = $(this).data("cart-id");  // ID корзины
        var $item = $(this).closest('.cart-item, tr');  // Элемент, который нужно удалить (может быть строка или блок)

        $.ajax({
            type: "POST",
            url: url,
            headers: {
                'X-CSRFToken': $("[name=csrfmiddlewaretoken]").val()
            },
            data: {
                cart_id: cartID
            },
            success: function(data) {
                // Удаляем элемент товара из корзины
                $item.remove();

                // Обновляем общие значения корзины
                $("#total-quantity").text(data.total_quantity);
                $("#total-price").text(data.total_price);
                $("#total-price-summary").text(data.total_price);
                $("#total-price-all").text(data.total_price);

                // Если нужно, обновляем мини-корзину
                var miniCart = $("#mini-cart");
                if (miniCart.length) {
                    miniCart.html(data.user_cart_html);
                }

                isProcessing = false;
            },
            error: function(data) {
                console.log("Ошибка при удалении товара");
                isProcessing = false;
            }
        });
    });
});
