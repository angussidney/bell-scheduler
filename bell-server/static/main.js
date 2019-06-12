let all_bells = [],
    selected_bells = [];

function Bell(time) { // todo keep going
    this.time = row.getElementsByTagName("td")[0].innerHTML;
    this.name = row.getElementsByTagName("td")[1].innerHTML;
    this.filepath = row.getElementsByTagName("td")[2].innerHTML;
    this.renderHTML = function () {
        return "<tr><td>" + this.time + "</td><td>" + this.name + "</td><td>" + this.filepath + "</td></tr>"
    }
}

function create_bell_from_html(row) {
    let time = row.getElementsByTagName("td")[0].innerHTML;
    let name = row.getElementsByTagName("td")[1].innerHTML;
    let filepath = row.getElementsByTagName("td")[2].innerHTML;
    return new Bell(time, name, filepath);
}

let bell_list = document.getElementById("bell-list");

function bell_in(bell_list, bell) {
    for (let i of bell_list) {
        if (i.name === bell.name) {
            return true
        }
    }
    return false
}

function toggle_controls() {
    document.getElementById("addnew").classList.toggle("d-hide");
    document.getElementById("editexisting").classList.toggle("d-hide");
}

bell_list.onclick = function (e) { // refactor to only take name - rest should be stored in data
    if (e.target.nodeName === "TD") {
        let bell = new Bell(e.target.parentNode);
        e.target.parentNode.classList.toggle('active');
        if (bell_in(selected_bells, bell)) {
            selected_bells = selected_bells.filter(function (item) {
                return item.name !== bell.name;
            });
            if (selected_bells.length === 0) {
                toggle_controls();
            }
        } else {
            if (selected_bells.length === 0) {
                toggle_controls();
            }
            selected_bells.push(bell)
        }
    }
};

function render_bells(data) {
    bell_list.innerHTML = "";
    for (let bell of data) {
        bell_list += bell.renderHTML();
    }
}

function add_bells() {
    // Get data from form
    document.querySelector("#addnew#bell-name")
    // Create bell and insert into list
    // Clear form and render data
}

function delete_bells() {
    // Remove selected bells from all_bells
    for (let bell of selected_bells) {
        all_bells = all_bells.filter(function (item) {
            return item.name !== bell.name;
        });
    }

    // Clear selected bells
    selected_bells = [];

    // Update table
    render_bells(all_bells);
    toggle_controls();
}
