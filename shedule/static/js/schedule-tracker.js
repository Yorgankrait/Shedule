const SCHEDULE = [
    { start: '08:30', end: '09:10', type: 'lesson', number: 1 },
    { start: '09:10', end: '09:30', type: 'break', number: 1 },
    { start: '09:30', end: '10:10', type: 'lesson', number: 2 },
    { start: '10:10', end: '10:30', type: 'break', number: 2 },
    { start: '10:30', end: '11:10', type: 'lesson', number: 3 },
    { start: '11:10', end: '11:30', type: 'break', number: 3 },
    { start: '11:30', end: '12:10', type: 'lesson', number: 4 },
    { start: '12:10', end: '12:30', type: 'break', number: 4 },
    { start: '12:30', end: '13:10', type: 'lesson', number: 5 },
    { start: '13:10', end: '13:30', type: 'break', number: 5 },
    { start: '13:30', end: '14:10', type: 'lesson', number: 6 },
    { start: '14:10', end: '14:30', type: 'break', number: 6 },
    { start: '14:30', end: '15:10', type: 'lesson', number: 7 },
    { start: '15:10', end: '15:30', type: 'break', number: 7 },
    { start: '15:30', end: '16:10', type: 'lesson', number: 8 }
];

function timeToMinutes(timeStr) {
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 60 + minutes;
}

function getCurrentPeriod() {
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    const currentMinutes = timeToMinutes(currentTime);

    for (const period of SCHEDULE) {
        const startMinutes = timeToMinutes(period.start);
        const endMinutes = timeToMinutes(period.end);

        if (currentMinutes >= startMinutes && currentMinutes < endMinutes) {
            if (period.type === 'lesson') {
                return `Сейчас идет ${period.number}-й урок`;
            } else {
                return `Сейчас перемена после ${period.number}-го урока`;
            }
        }
    }

    if (currentMinutes < timeToMinutes(SCHEDULE[0].start)) {
        return 'Уроки еще не начались';
    }
    if (currentMinutes >= timeToMinutes(SCHEDULE[SCHEDULE.length - 1].end)) {
        return 'Уроки закончились';
    }

    return 'Вне учебного времени';
}

function updateCurrentPeriod() {
    const currentPeriodElement = document.getElementById('current-period');
    if (currentPeriodElement) {
        currentPeriodElement.textContent = getCurrentPeriod();
    }
}

// Обновляем информацию каждую минуту
setInterval(updateCurrentPeriod, 60000);

// Запускаем сразу при загрузке страницы
document.addEventListener('DOMContentLoaded', updateCurrentPeriod); 