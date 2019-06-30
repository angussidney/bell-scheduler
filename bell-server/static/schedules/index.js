document.addEventListener('DOMContentLoaded', function () {
    let calendarEl = document.getElementById('calendar');

    let calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['dayGrid', 'interaction'],
        defaultView: 'dayGridMonth',
        selectable: true,
        events: '/schedule/list.json',

        select: function(info) {
            document.getElementById("delete_button").classList.remove("d-hide");
            document.getElementById("start").value = info.startStr;
            document.getElementById("end").value = info.endStr;
        },
        unselect: function() {
            document.getElementById("delete_button").classList.add("d-hide");
        }
    });

    calendar.render();

    calendar.updateSize();
});