document.addEventListener('DOMContentLoaded', function () {
    let calendarEl = document.getElementById('calendar');

    let calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['dayGrid'],
        defaultView: 'dayGridWeek',
        events: '/schedule/list.json',
        aspectRatio: 8
    });

    calendar.render();

    calendar.updateSize();
});