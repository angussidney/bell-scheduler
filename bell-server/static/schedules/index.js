document.addEventListener('DOMContentLoaded', function() {
    let calendarEl = document.getElementById('calendar');

    let calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['dayGrid', 'interaction'],
        defaultView:'dayGridMonth',
        selectable: true,
        events: '/schedule/list.json'
    });

    calendar.render();

    calendar.updateSize();
});