// TODO: Use actual date obj instead of string - or not?
// TODO: use forEach instead of for-of
// TODO: Separate javascript into multiple files

let all_bells = [], // List of bell objects
    selected_bells = []; // List of names

function Bell(time, name, sound, sound_id) {
    this.time = time;
    this.name = name;
    this.sound = sound;
    this.sound_id = sound_id;
    this.renderHTML = function () {
        return "<tr><td>" + this.time + "</td><td>" + this.name + "</td><td>" + this.sound + "</td></tr>"
    }
}

function get_bell_by_name(bell_name) {
    for (let bell of all_bells) {
        if (bell.name === bell_name) {
            return bell;
        }
    }
    return null;
}

function get_bell_by_time(time) {
    for (let bell of all_bells) {
        if (bell.time === time) {
            return bell;
        }
    }
    return null;
}

let bell_list_el = document.getElementById("bell-list");

function toggle_controls() {
    document.getElementById("addnew").classList.toggle("d-hide");
    document.getElementById("editexisting").classList.toggle("d-hide");
}

bell_list_el.onclick = function (e) { // refactor to only take name - rest should be stored in data
    if (e.target.nodeName === "TD") {
        let bell_name = e.target.parentNode.childNodes[1].innerHTML;
        e.target.parentNode.classList.toggle('active');
        let index = selected_bells.indexOf(bell_name);
        if (index !== -1) {
            // Bell already selected
            selected_bells.splice(index, 1);
            if (selected_bells.length === 0) {
                toggle_controls();
            } else if (selected_bells.length === 1) {
                document.getElementById("edit").classList.toggle("d-hide");
            }
        } else {
            if (selected_bells.length === 0) {
                toggle_controls();
            } else if (selected_bells.length === 1) {
                document.getElementById("edit").classList.toggle("d-hide");
            }
            selected_bells.push(bell_name)
        }
    }
};

function render_bells(data) {
    if (data.length > 0) {
        bell_list_el.innerHTML = "";
        for (let bell of data) {
            bell_list_el.innerHTML += bell.renderHTML();
        }
    } else if (document.querySelector("#addnew #bell-name").value === "") {
        // Table is actually empty
        bell_list_el.innerHTML = "<tr><td colspan='3' class='text-center'><em>There are currently no bells scheduled.</em></td></tr>"
    } else {
        bell_list_el.innerHTML = "<tr><td colspan='3' class='text-center'><em>You are currently editing the only bell.</em></td></tr>"
    }
}

function report_error(el, text) {
    let warn = document.getElementById('add_warnings');
    warn.classList.remove('d-hide');
    warn.innerText = text;

    el.dispatchEvent(new Event('invalid'));
    el.classList.add('is-error');
}

function add_bells() {
    // Get data from form
    let time = document.querySelector("#addnew #bell-time");
    let name = document.querySelector("#addnew #bell-name");
    let file = document.querySelector("#addnew #bell-file");

    // TODO: Disallow same name/same time, or empty fields
    // time.setCustomValidity("No two bells can be scheduled for the same time");
    // name.setCustomValidity("No two bells can have the same name");

    // Remove warnings
    time.classList.remove('is-error');
    name.classList.remove('is-error');
    document.getElementById('add_warnings').classList.add('d-hide');

    if (time.value === "") {
        report_error(time, "Please fill out this field.");
    } else if (!time.checkValidity()) {
        report_error(time, "That is not a valid time format. Please use 24-hour time e.g. 13:55");
    } else if (get_bell_by_time(time.value)) {
        report_error(time, "There is already a bell scheduled for that time.");
    } else if (name.value === "") {
        report_error(name, "Please fill out this field.");
    } else if (get_bell_by_name(name.value)) {
        report_error(name, "There is already a bell with that name.");
    } else { // All fields are valid
        // Sort into list
        let new_bell = new Bell(time.value, name.value, file.options[file.selectedIndex].text, file.value);
        let inserted = false;
        for (let i = 0; i < all_bells.length; i++) {
            if (all_bells[i].time > new_bell.time) {
                all_bells = all_bells.slice(0, i).concat(new_bell, all_bells.slice(i));
                inserted = true;
                break;
            }
        }
        if (!inserted) {
            all_bells.push(new_bell);
        }

        // Clear form and render data
        time.value = "";
        name.value = "";
        file.selectedIndex = 0;
        document.getElementById("add").innerHTML = "Add";
        render_bells(all_bells);
    }
}

function edit_bells() {
    // Prefill the 'add new' form
    let bell = get_bell_by_name(selected_bells[0]);
    document.querySelector("#addnew #bell-time").value = bell.time;
    document.querySelector("#addnew #bell-name").value = bell.name;
    document.querySelector("#addnew #bell-file").value = bell.sound_id;

    // Remove the bell from the table
    all_bells = all_bells.filter(function (item) {
        return item.name !== bell.name;
    });

    // Re-render form for editing
    render_bells(all_bells);
    toggle_controls();
    document.getElementById("add").innerHTML = "Save";
    selected_bells = [];
}

function delete_bells() {
    // Remove selected bells from all_bells
    for (let bell_name of selected_bells) {
        all_bells = all_bells.filter(function (item) {
            return item.name !== bell_name;
        });
    }

    // Clear selected bells
    if (selected_bells.length > 1) {
        document.getElementById("edit").classList.toggle("d-hide");
    }
    selected_bells = [];

    // Update table
    render_bells(all_bells);
    toggle_controls();
}


new Cleave('#bell-time', {
    time: true,
    timePattern: ['h', 'm']
});


// TODO: Require at least one box to be checked
document.getElementById("apply").onclick = function (ev) {
    let checked = document.getElementById("apply").checked;
    document.querySelectorAll("input[name='apply_to']").forEach(function (el) {
        el.disabled = !checked;
        el.checked = false;
    });
    // TODO: Fill warnings in modal
};

function toggle_modal(id) {
    document.getElementById(id).classList.toggle("active");
}

function assemble_data() {
    all_bells.forEach(function (bell) {
        // Surely there's a better way to do this without repeating myself?
        let time = document.createElement('input');
        time.type = 'hidden';
        time.name = 'bell_times';
        time.value = bell.time;
        document.forms['template_form'].appendChild(time);

        let name = document.createElement('input');
        name.type = 'hidden';
        name.name = 'bell_names';
        name.value = bell.name;
        document.forms['template_form'].appendChild(name);

        let sound_id = document.createElement('input');
        sound_id.type = 'hidden';
        sound_id.name = 'bell_sound_ids';
        sound_id.value = bell.sound_id;
        document.forms['template_form'].appendChild(sound_id);
    });
}

function toggle_default_warnings() {
    [].forEach.call(document.getElementsByClassName("default_toggle"), function (el) {
        console.log("ping");
        el.classList.toggle("d-hide");
    });
}

function hide_this(ev) {
    ev.target.parentNode.classList.add('d-hide');
}

function change_action(form_id, url) {
    document.getElementById(form_id).setAttribute("action", url);
}
