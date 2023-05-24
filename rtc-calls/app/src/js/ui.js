let callTab = document.getElementById("callTab");
let miroTab = document.getElementById("miroTab");

let callPanel = document.getElementById("callPanel");
let miroPanel = document.getElementById("miroPanel");

let localVideo = document.getElementById("localVideo");
let remoteVideo = document.getElementById("remoteVideo");

let chatTab = document.getElementById("chatTab");
let marksTab = document.getElementById("marksTab");

let active_main_tab = callTab;
let active_mini_tab = chatTab;

function change_main_tab() {
    active_main_tab.classList.remove("tab-active");
    if (active_main_tab == callTab) {
        active_main_tab = miroTab;

        callPanel.hidden = true;
        miroPanel.hidden = false;
    } else if (active_main_tab == miroTab) {
        active_main_tab = callTab;

        miroPanel.hidden = true;
        callPanel.hidden = false;
    }
    active_main_tab.classList.add("tab-active");
}

function change_mini_tab() {
    active_mini_tab.classList.remove("tab-active");
    if (active_mini_tab == chatTab) {
        active_mini_tab = marksTab;
    } else if (active_mini_tab == marksTab) {
        active_mini_tab = chatTab;
    }
    active_mini_tab.classList.add("tab-active");
}

let left_panel = document.getElementById("leftPanel");
let right_panel = document.getElementById("rightPanel");
let marks_panel = document.getElementById("rightPanelMark");

let is_leftPanel = false;
let is_marksPanel = false;


function open_close_marks_panel() {
    if (is_leftPanel) {
        open_close_right_panel();
    }

    if (is_marksPanel) {
        left_panel.classList.remove("col-9");
        left_panel.classList.add("col-10");

        marks_panel.hidden = true;
        is_marksPanel = false;
    } else {
        left_panel.classList.remove("col-10");
        left_panel.classList.add("col-9");

        marks_panel.hidden = false;
        is_marksPanel = true;
    }
}

function open_close_right_panel() {
    if (is_marksPanel) {
        open_close_marks_panel();
    }

    if (is_leftPanel) {
        right_panel.hidden = true;

        left_panel.classList.remove("col-9");
        left_panel.classList.add("col-10");

        is_leftPanel = false;
    } else {
        left_panel.classList.remove("col-10");
        left_panel.classList.add("col-9");

        right_panel.hidden = false;
        is_leftPanel = true;
    }
}

document.getElementById("chatbtn").addEventListener("click", function() {
    open_close_right_panel();
});

document.getElementById("marksbtn").addEventListener("click", function() {
    open_close_marks_panel();
});