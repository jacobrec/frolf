const server = "http://localhost:8888";

function get(path, callback) {
    var myRequest = new XMLHttpRequest();
    myRequest.open('GET', server + path);
    myRequest.onreadystatechange = function () {
        if (myRequest.readyState === 4) {
            callback(myRequest.responseText);
        }
    };
    myRequest.send();
}

function post(path, data, callback) {
    var myRequest = new XMLHttpRequest();
    myRequest.open('POST', server + path);
    myRequest.onreadystatechange = function () {
        if (myRequest.readyState === 4) {
            callback(myRequest.responseText);
        }
    };
    myRequest.send(data);
}

function sync() {
    syncGames();
    syncNames();
    syncCourses();
}

function syncGames() {
    let todo = JSON.parse(localStorage.getItem("tosync") || "[]");
    for (let game of todo) {
        let send_data = JSON.stringify({
            "time": game.time
            , "pids": game.info.players
            , "scores": game.scores.slice(1).map((v, i, a) => v.score)
            , "cid": game.info.course
        });
        //console.log(send_data);
        post("/game/" + localStorage.getItem("groupid"), send_data, (data) => {
            let all = JSON.parse(localStorage.getItem("tosync") || "[]");
            for (let i in all) {
                if (all[i].time == game.time) {
                    let after = all.filter((v, ind, a) => ind != i);
                    localStorage.setItem("tosync", JSON.stringify(after));
                    break;
                }
            }
        });
    }
}

function syncNames() {
    get("/group/players/" + localStorage.getItem("groupid"), function (data) {
        localStorage.setItem("names", data);
    });
}

function syncCourses() {
    get("/group/courses/" + localStorage.getItem("groupid"), function (data) {
        localStorage.setItem("courses", data);
    });
}