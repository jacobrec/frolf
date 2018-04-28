/* jslint browser: true */
function setLogoCss() {
    let unit = "vw";
    if (window.screen.width > window.screen.height) {
        unit = "vh";
    }
    document.getElementById("logo").style.width = "60" + unit;
    document.getElementById("logo").style.margin = "5" + unit;
}

function setButtonLoc() {
    document.getElementById("newgame").style.position = "absolute";
    document.getElementById("newgame").style.bottom = "5vh";
}

function logout() {
    localStorage.removeItem("groupid");
    window.location.href = server;
}
window.onload = function () {
    M.AutoInit();
    M.Sidenav.init(document.querySelector('.sidenav'), {});
    if (localStorage.getItem("groupid") == null) {
        document.getElementById("newgame").style.display = "none";
        document.getElementById("signin").style.display = "block";
    }
    setLogoCss();
    setButtonLoc();
    sync();
}