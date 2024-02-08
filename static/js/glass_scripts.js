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

    // Обработчик события клика по кнопке
    $('.glass').each(function(index) {
        var element = $(this);

        // Получаем текущий индекс для данного элемента из localStorage
        var currentIndex = parseInt(localStorage.getItem('glassIndex_' + index)) || 0;

        // Меняем фон только текущего элемента
        element.css('background-image', 'url(' + imagePaths[currentIndex] + ')');

        // Сохраняем текущий индекс для данного элемента
        element.data('currentIndex', currentIndex);

        // Обработчик события клика по текущему элементу
        element.click(function() {
            // Проверяем, не является ли текущий индекс последним
            if (currentIndex < imagePaths.length - 1) {
                currentIndex++;
                // Меняем фон только текущего элемента
                element.css('background-image', 'url(' + imagePaths[currentIndex] + ')');
                
                // Сохраняем текущий индекс для данного элемента в localStorage
                localStorage.setItem('glassIndex_' + index, currentIndex);

                // Сохраняем текущий индекс для данного элемента
                element.data('currentIndex', currentIndex);
            }
        });
    });
});
