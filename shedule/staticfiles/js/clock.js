function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    
    const timeString = `${hours}:${minutes}:${seconds}`;
    
    // Обновляем оба элемента часов
    document.getElementById('clock').textContent = timeString;
    const mobileClock = document.getElementById('clock-mobile');
    if (mobileClock) {
        mobileClock.textContent = timeString;
    }
}

// Обновляем время каждую секунду
setInterval(updateClock, 1000);

// Запускаем часы сразу при загрузке страницы
updateClock(); 