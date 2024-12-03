$(document).ready(function() {
    $('form').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    // Показываем уведомление
                    $('.notification').show();
                    // Ждем 3 секунды и затем переходим на новую страницу
                    setTimeout(function() {
                        window.location.href = response.redirect_url;
                    }, 3000);
                }
            }
        });
    });
});
