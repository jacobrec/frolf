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


@app.get("/group/<string>/<string>")
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
    player["handicap"] = golf.handicap([json.loads(x[2]) for x in games], [json.loads(x[4]) for x in games])

    return json.dumps(player)


@app.get("/games/<int>")
def getGameById(gid):
    game = {}
    stats = db.getGame(gid)
    game["time"] = stats[0][3]
    game["players"] = [x[0] for x in stats]
    game["scores"] = [x[1] for x in stats]
    course = db.getCourse(stats[0][2])
    game["course"] = {"id": stats[0][2], "pars": course[0],"name":course[1]}
    return json.dumps(game)

@app.get("/course/<int>")
def getCourseById(cid):
    return json.dumps(db.getCourse(cid))


@app.post("/game/<int>")
def addNewGame(data, grid):
    pass


@app.post("/course/<int>")
def addNewCourse(data, grid):
    pass

@app.post("players/<int>")
def addNewPlayer(data, grid):
    pass


@app.get("/", content_type="text/plain")
def welcome():
    return """Welcome to the frisbee golf app. If you're seeing this page, you're using it wrong. Please use the app"""

app.listen(8888)
