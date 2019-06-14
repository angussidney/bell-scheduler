// TODO: Use actual date obj instead of string

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

function bell_in(bell_list, bell_name) {
    for (let i of bell_list) {
        if (i.name === bell_name) {
            return true
        }
    }
    return false
}

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
            }
        } else {
            if (selected_bells.length === 0) {
                toggle_controls();
            }
            selected_bells.push(bell_name)
        }
    }
};

function render_bells(data) {
    bell_list_el.innerHTML = "";
    for (let bell of data) {
        bell_list_el += bell.renderHTML();
    }
}

function add_bells() {
    // Get data from form
    let time = document.querySelector("#addnew #bell-time");
    let name = document.querySelector("#addnew #bell-name");
    let file = document.querySelector("#addnew #bell-file");

    all_bells.push(new Bell(time, name, file));

    // Clear form and render data
    document.querySelector("#addnew #bell-time").value;
    document.querySelector("#addnew #bell-name");
    document.querySelector("#addnew #bell-file");
}

function delete_bells() {
    // Remove selected bells from all_bells
    for (let bell_name of selected_bells) {
        all_bells = all_bells.filter(function (item) {
            return item.name !== bell_name;
        });
    }

    // Clear selected bells
    selected_bells = [];

    // Update table
    render_bells(all_bells);
    toggle_controls();
}
