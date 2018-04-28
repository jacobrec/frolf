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
    // TODO: clean this up at some point, it's a mess
    let todo = JSON.parse(localStorage.getItem("tosync") || "[]");
    for (let g in todo) {
        let game = todo[g];
        console.log(game);
        if (game.info.newStuff.players.length > 0) {
            let p = 0;
            post("/players/" + localStorage.getItem("groupid"), JSON.stringify({
                "name": game.info.newStuff.players[p]
            }), (data) => {
                game.info.players = game.info.players.map((v, i, a) => (game.info.newStuff.players[p] == v ? JSON.parse(data).pid : v));
                game.info.newStuff.players = game.info.newStuff.players.filter((v, i, a) => p != i);
                todo[g] = game;
                localStorage.setItem("tosync", JSON.stringify(todo));
                syncGames();
            });
        }
        else if (game.info.newStuff.courses.length > 0) {
            if (game.info.newStuff.courses == game.info.course) {
                post("/course/" + localStorage.getItem("groupid"), JSON.stringify({
                    "pars": game.scores[0].score
                    , "name": game.info.newStuff.courses[0]
                }), (data) => {
                    game.info.course = JSON.parse(data).cid;
                    game.info.newStuff.courses = [];
                    todo[g] = game;
                    localStorage.setItem("tosync", JSON.stringify(todo));
                    syncGames();
                });
            }
        }
        else {
            sendGame(game);
        }
    }
}

function sendGame(game) {
    let send_data = JSON.stringify({
        "time": game.time
        , "pids": game.info.players
        , "scores": game.scores.slice(1).map((v, i, a) => v.score)
        , "cid": game.info.course
    });
    console.log(send_data);
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