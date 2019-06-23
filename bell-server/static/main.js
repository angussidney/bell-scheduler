// TODO: Use actual date obj instead of string - or not?
// TODO: use forEach instead of for-of
// TODO: Separate javascript into multiple files

let all_bells = [], // List of bell objects
    selected_bells = []; // List of names

function Bell(time, name, filepath) {
    this.time = time;
    this.name = name;
    this.filepath = filepath;
    this.renderHTML = function () {
        return "<tr><td>" + this.time + "</td><td>" + this.name + "</td><td>" + this.filepath + "</td></tr>"
    }
}

function get_bell(bell_name) {
    for (let bell of all_bells) {
        if (bell.name === bell_name) {
            return bell
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
        bell_list_el.innerHTML = "<tr><td colspan='3' style='text-align: center'><em>There are currently no bells scheduled.</em></td></tr>"
    } else {
        bell_list_el.innerHTML = "<tr><td colspan='3' style='text-align: center'><em>You are currently editing the only bell.</em></td></tr>"
    }
}

function add_bells() {
    // Get data from form
    let time = document.querySelector("#addnew #bell-time").value;
    let name = document.querySelector("#addnew #bell-name").value;
    let file = document.querySelector("#addnew #bell-file").value;

    // TODO: Disallow same name/same time, or empty fields
    // time.setCustomValidity("No two bells can be scheduled for the same time");
    // name.setCustomValidity("No two bells can have the same name");

    // Sort into list
    let new_bell = new Bell(time, name, file);
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
    document.querySelector("#addnew #bell-time").value = "";
    document.querySelector("#addnew #bell-name").value = "";
    document.querySelector("#addnew #bell-file").selectedIndex = 0;
    document.getElementById("add").innerHTML = "Add";
    render_bells(all_bells);
}

function edit_bells() {
    // Prefill the 'add new' form
    let bell = get_bell(selected_bells[0]);
    document.querySelector("#addnew #bell-time").value = bell.time;
    document.querySelector("#addnew #bell-name").value = bell.name;
    document.querySelector("#addnew #bell-file").value = bell.filepath;

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
        document.forms['template_form'].appendChild(time);

        let filepath = document.createElement('input');
        filepath.type = 'hidden';
        filepath.name = 'bell_filepaths';
        filepath.value = bell.filepath;
        document.forms['template_form'].appendChild(time);
    });
}

function toggle_default_warnings() {
    [].forEach.call(document.getElementsByClassName("default_toggle"), function (el) {
        console.log("ping");
        el.classList.toggle("d-hide");
    });
}

function hide_this(el) {
    el.parent.classList.add('d-hide');
}