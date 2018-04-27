import json
import golf

from api import PocketTornado
import sql


app = PocketTornado()
app.default_content = "application/json"
db = sql.DatabaseManager(*sql.loginInfo())


@app.get("/group/players/<int>")
def getPlayersFromGroup(grid):
    return json.dumps(db.getPlayersByGroup(grid))


@app.get("/group/courses/<int>")
def getCoursesFromGroup(grid):
    return json.dumps(db.getCoursesByGroup(grid))


@app.get("/login/<string>/<string>")
def getGroupByLogin(user, pw):
    group = db.getGroupByLogin(user, pw)
    print(group)
    if group is None:
        return ""
    else:
        return json.dumps(group)


@app.get("/group")
def getGroupList():
    return json.dumps(db.getGroups())


@app.get("/player/<int>")
def getPlayersById(pid):
    player = {}
    player["name"] = db.getPlayerName(pid)

    games = db.getAllGamesByPlayer(pid)
    player["games"] = [x[3] for x in games]
    player["handicap"] = golf.handicap([json.loads(x[2]) for x in games], [
                                       json.loads(x[4]) for x in games])

    return json.dumps(player)


@app.get("/games/<int>")
def getGameById(gid):
    game = {}
    stats = db.getGame(gid)
    game["time"] = stats[0][3]
    game["players"] = [x[0] for x in stats]
    game["scores"] = [x[1] for x in stats]
    course = db.getCourse(stats[0][2])
    game["course"] = {"id": stats[0][2], "pars": course[0], "name": course[1]}
    return json.dumps(game)


@app.get("/course/<int>")
def getCourseById(cid):
    course = {}
    c = db.getCourse(cid)
    course["name"] = c[1]
    course["par"] = c[0]
    r = db.getRecentGamesAtCourse(cid)
    a = {} 
    for x in r: # time, gid, pid, cid
        gid = x[1]
        if gid in a:
            a[gid]["pid"].append(x[2])
        else:
            a[gid] = {"time": x[0], "gid": x[1], "pid": [x[2]], "cid": x[3]} 

    course["recent"] = list(a.values())
    return json.dumps(course)


@app.post("/game/<int>")
def addNewGame(data, grid):
    pass


@app.post("/course/<int>")
def addNewCourse(data, grid):
    pass


@app.post("players/<int>")
def addNewPlayer(data, grid):
    pass


app.static("/<all>", r"client/", remap={"/": "index.html"})

app.listen(8888, debug=True)
