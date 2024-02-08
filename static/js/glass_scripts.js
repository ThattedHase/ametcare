$(document).ready(function() {
    // Список путей к изображениям
    var imagePaths = [
        '/static/img/glass1.png',
        '/static/img/glass2.png',
        '/static/img/glass3.png',
        '/static/img/glass4.png',
        '/static/img/glass5.png',
        '/static/img/glass6.png',
        '/static/img/glass7.png'
    ];

    // Получаем уникальный идентификатор пользователя
    var userId = '{{ current_user.id }}';  // замените на ваш способ получения идентификатора пользователя

    // Обработчик события клика по кнопке
    $('.glass').each(function(index) {
        var element = $(this);

        // Получаем текущий индекс для данного элемента
        var currentIndex = parseInt(element.data('currentIndex')) || 0;

        // Меняем фон только текущего элемента
        element.css('background-image', 'url(' + imagePaths[currentIndex] + ')');

        // Обработчик события клика по текущему элементу
        element.click(function() {
            // Проверяем, не является ли текущий индекс последним
            if (currentIndex < imagePaths.length - 1) {
                currentIndex++;
                // Меняем фон только текущего элемента
                element.css('background-image', 'url(' + imagePaths[currentIndex] + ')');
                
                // Отправляем текущий индекс для данного элемента на сервер
                $.ajax({
                    type: 'POST',
                    url: '/update_glass_index',  // Замените на ваш URL для обновления индекса
                    data: { userId: userId, glassIndex: index, currentIndex: currentIndex },
                    success: function(response) {
                        // Обработка успешного ответа, если необходимо
                    },
                    error: function(error) {
                        console.error('Ошибка при отправке данных на сервер:', error);
                    }
                });
            }
        });
    });
});
