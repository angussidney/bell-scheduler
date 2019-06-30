document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('input[type="date"]').forEach(function (el) {
        el.setAttribute('min', new Date().toISOString().split("T")[0]);
        new Cleave(el, {
            date: true,
            delimiter: '-',
            datePattern: ['Y', 'm', 'd']
        });
    });

    add_single_date();
});

let dates_list = document.getElementById('dates_list');
let next_index = 0;
let empty_text = "<li>" +
    "<em>You have not added any dates. Please add at least one date or date range using the buttons below.</em>" +
    "</li>";
let empty = false;

function add_single_date() {
    if (empty) {
        dates_list.innerHTML = "";
    }
    let html = '<li class="single_date">' +
        '<label class="form-label" for="start' + next_index + '">Single date:</label>' +
        '<input type="date" class="form-input" name="start" id="start' + next_index + '" placeholder="yyyy-mm-dd" pattern="[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])" min="' + new Date().toISOString().split("T")[0] + '" required>' +
        '<button type="button" class="btn btn-link btn-action btn-lg text-error" onclick="delete_date(event)"><i class="icon icon-close"></i></button>' +
        '</li>';
    dates_list.insertAdjacentHTML('beforeend', html);
    next_index += 1;
    empty = false;
}

function add_date_range() {
    if (empty) {
        dates_list.innerHTML = "";
    }
    let html = '<li class="date_range">' +
        '<label class="form-label" for="start' + next_index + '">From:</label>' +
        '<input type="date" class="form-input" name="start" id="start' + next_index + '" placeholder="yyyy-mm-dd" pattern="[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])" min="' + new Date().toISOString().split("T")[0] + '" required>' +
        '<label class="form-label" for="end' + next_index + '">to:</label>' +
        '<input type="date" class="form-input" name="end" id="end' + next_index + '" placeholder="yyyy-mm-dd" pattern="[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])" min="' + new Date().toISOString().split("T")[0] + '" required>' +
        '<button type="button" class="btn btn-link btn-action btn-lg text-error" onclick="delete_date(event)"><i class="icon icon-close"></i></button>' +
        '</li>';
    dates_list.insertAdjacentHTML('beforeend', html);
    next_index += 1;
    empty = false;
}

function delete_date(ev) {
    let list_item;
    if (ev.target.nodeName === "I") {
        list_item = ev.target.parentNode.parentNode;
    } else {
        list_item = ev.target.parentNode;
    }
    list_item.parentNode.removeChild(list_item);

    if (dates_list.getElementsByTagName("li").length === 0) {
        dates_list.innerHTML = empty_text;
        empty = true;
    }
}

function check_dates() {
    if (empty) {
        add_single_date();
        // Form validation will now pick up the empty field and reject submission
    }
}

function complete_single_dates() {
    dates_list.querySelectorAll("li").forEach(function (el) {
        if (el.classList.contains('single_date')) {
            let end = document.createElement('input');
            end.type = 'hidden';
            end.name = 'end';
            end.value = el.childNodes[1].value;
            el.appendChild(end);
        }
    });
}