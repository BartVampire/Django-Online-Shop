
$(document).ready(function() {
    /**
     * Обновление деталей товара
     *
     */
    function updateVariantDetails(data) {
        console.log("Updating variant details:", data);
        $('#selected-color').text(data.color || '');
        $('#selected-size').text(data.size || '');
        $('#price').text((data.price || '0') + ' руб.');
        $('#discount-percentage').text((data.discount || '0') + '%');
        $('#sell-price').text((data.sell_price || '0') + ' руб.');
        $('#article').text(data.article || '');
        $('#stock').html(data.stock > 0 ? '<span class="instock">В наличии</span>' : '<span class="instock" style="color: red">Нет в наличии</span>');
        
        updateOptions('#color-options', data.available_colors, 'color');
        updateOptions('#size-options', data.available_sizes, 'size');
        
        if (parseFloat(data.discount) != 0) {
            $('#ComparePrice-product-template').show();
            $('.discount-badge').show();
        } else {
            $('#ComparePrice-product-template').hide();
            $('.discount-badge').hide();
        }
    }

    function updateOptions(container, options, type) {
        console.log(`Updating ${type} options:`, options);
        $(container).empty();
        options.forEach(function(option) {
            var isSelected = (type === 'color' && option === $('#selected-color').text()) || 
                             (type === 'size' && option === $('#selected-size').text());
            var style = isSelected ? 'style="background-color:lightgray;"' : '';
            $(container).append(`<button type="button" class="${type}-option btn" data-${type}="${option}" ${style}>${option}</button>`);
        });
    }

    function getVariants(color, size) {
        console.log(`Getting variants for color: ${color}, size: ${size}`);
        $.ajax({
            url: '{% url "get_product_variants" product_detail.slug %}',
            data: { color: color, size: size },
            success: function(data) {
                console.log("Received data:", data);
                updateVariantDetails(data);
            },
            error: function(xhr, status, error) {
                console.error("Error fetching variants:", error);
            }
        });
    }

    $(document).on('click', '.color-option', function() {
        var color = $(this).data('color');
        var size = $('#selected-size').text();
        console.log(`Color option clicked: ${color}`);
        getVariants(color, size);
    });

    $(document).on('click', '.size-option', function() {
        var size = $(this).data('size');
        var color = $('#selected-color').text();
        console.log(`Size option clicked: ${size}`);
        getVariants(color, size);
    });

    // Инициализация при загрузке страницы
    var initialColor = $('#selected-color').text();
    var initialSize = $('#selected-size').text();
    getVariants(initialColor, initialSize);
});


