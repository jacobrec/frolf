import pymysql
import time
import json


class DatabaseManager():
    def __init__(self, username, password, database):
        self.conn = pymysql.connect(
            user=username, password=password, db=database)
        self.cur = self.conn.cursor()

    def getGroups(self):
        self.cur.execute("SELECT (name) FROM groups")
        return [x[0] for x in self.cur.fetchall()]

    def getGroupByLogin(self, name, password):
        self.cur.execute(
            "SELECT (grid, password) FROM groups WHERE name = {}".format(
                grid.strip()))
        (g, p) = self.cur.fetchone()
        if p != password:
            return
        return g

    def getPlayersByGroup(self, grid):
        self.cur.execute("SELECT (pid, name) FROM users WHERE grid = {}".format(grid))
        return self.cur.fetchall()

    def getCoursesByGroup(self, grid):
        self.cur.execute("SELECT (cid, pars, name) FROM courses WHERE grid = {}".format(grid))
        return self.cur.fetchall()

    def getPlayerName(self, pid):
        self.cur.execute("SELECT (name) FROM users WHERE pid = {}".format(pid))
        return self.cur.fetchone()

    def getGameTime(self, gid):
        self.cur.execute("SELECT (time) FROM games WHERE gid = {}".format(gid))
        return self.cur.fetchone()

    def getCourse(self, cid):
        self.cur.execute("SELECT (pars, name) FROM courses WHERE cid = {}".format(cid))
        return self.cur.fetchone()

    def putGame(self, pids, scores, cid, grid):
        self.cur.execute(
            "INSERT INTO games (cid, time, grid) VALUES({}, {}, {})".format(
                cid, int(time.time()), grid))
        self.cur.execute("SELECT LAST_INSERT_ID()")
        gid = self.cur.fetchone()[0]
        for x in range(len(pids)):
            self.cur.execute(
                "INSERT INTO player_game(pid, gid, scores) VALUES({}, {}, '{}')" .format(
                    pids[x], gid, json.dumps(
                        scores[x])))
        self.conn.commit()

    def putCourse(self, pars, name, grid):
        cur.execute('INSERT INTO courses(pars, name, grid) VALUES("{}",{}, {})'
                    .format(json.dumps(pars), name, grid))
        self.conn.commit()



def loginInfo():
    """
    parses .password file and returns login info
    """

    try:
        serverinfoFile = open(".password", 'r')
        username = serverinfoFile.readline().strip()
        pw = serverinfoFile.readline().strip()
        database = serverinfoFile.readline().strip()
    except FileNotFoundError:
        serverinfoFile = open(".password", 'w')
        username = input("mysql username:")
        pw = input("mysql password:")
        database = input("mysql database:")
        serverinfoFile.write(username + "\n")
        serverinfoFile.write(pw + "\n")
        serverinfoFile.write(database + "\n")

    return (username, pw, database)