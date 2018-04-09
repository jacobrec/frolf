import json

from api import PocketTornado
import sql


app = PocketTornado()
app.default_content = "application/json"
db = sql.DatabaseManager(*sql.loginInfo())

@app.get("/group/players/<int>")
def getPlayersFromGroup(grid):
    pass


@app.get("/group/courses/<int>")
def getCoursesFromGroup(grid):
    pass


@app.get("/group/<string>/<string>")
def getGroupByLogin(user, pw):
    pass


@app.get("/group")
def getGroupList():
    return json.dumps(db.getGroups())


@app.get("/player/<int>")
def getPlayersById(pid):
    pass


@app.get("/games/<int>")
def getGameById(gid):
    pass


@app.get("/course/<int>")
def getCourseById(cid):
    pass


@app.post("/game/<int>")
def addNewGame(data, grid):
    pass


@app.post("/course/<int>")
def addNewCourse(data, grid):
    pass

@app.get("/", content_type="text/plain")
def welcome():
    return """Welcome to the frisbee golf app. If you're seeing this page, you're using it wrong. Please use the app"""

app.listen(8888)
