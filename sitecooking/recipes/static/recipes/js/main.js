$(document).ready(function() {
        $('#add-post-form').on('submit', function(event) {
            event.preventDefault(); // Предотвращаем стандартное поведение формы

            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                data: $(this).serialize(),
                success: function(response) {
                    $('#form-messages').html('<p>Рецепт добавлен! ID: ' + response.post_id + '</p>');
                    $('#add-post-form')[0].reset(); // Сброс формы
                },
                error: function(xhr) {
                    var errors = xhr.responseJSON.errors;
                    var errorMessages = '<ul>';
                    $.each(errors, function(key, value) {
                        errorMessages += '<li>' + value.join(', ') + '</li>';
                    });
                    errorMessages += '</ul>';
                    $('#form-messages').html('<p>Ошибка при добавлении рецепта:</p>' + errorMessages);
                }
            });
        });
    });