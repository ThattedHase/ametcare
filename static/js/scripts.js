const cards = document.querySelectorAll('.card');
let currentCardIndex = 0;
const cards1 = document.querySelectorAll('.card1');
let currentCardIndex1 = 0;
const cards2 = document.querySelectorAll('.card2'); // Добавляем выбор третьей стопки карт
let currentCardIndex2 = 0; // Создаем переменную для третьей стопки

function showCard(index) {
    cards.forEach((card, i) => {
        if (i === index) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function showCard1(index) {
    cards1.forEach((card, i) => {
        if (i === index) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function showCard2(index) {
    cards2.forEach((card, i) => {
        if (i === index) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

showCard(currentCardIndex);
showCard1(currentCardIndex1);
showCard2(currentCardIndex2); // Вызываем функцию для третьей стопки

cards1.forEach((card, i) => {
    card.addEventListener('click', () => {
        currentCardIndex1 = (i + 1) % cards1.length;
        showCard1(currentCardIndex1);
    });
});

cards.forEach((card, i) => {
    card.addEventListener('click', () => {
        currentCardIndex = (i + 1) % cards.length;
        showCard(currentCardIndex);
    });
});

cards2.forEach((card, i) => {
    card.addEventListener('click', () => {
        currentCardIndex2 = (i + 1) % cards2.length; // Управление третьей стопкой карт
        showCard2(currentCardIndex2);
    });
});
