import pymysql
import time
import json


class DatabaseManager():
    def __init__(self, username, password, database):
        self.conn = pymysql.connect(
            user=username, password=password, db=database)
        self.cur = self.conn.cursor()

    def getGroupByName(self, name):
        self.cur.execute(
            "SELECT * FROM groups WHERE name = {}".format(grid.strip()))
        return self.cur.fetchone()

    def getPlayersByGroup(self, grid):
        self.cur.execute("SELECT * FROM users WHERE grid = {}".format(grid))
        return self.cur.fetchall()

    def getCoursesByGroup(self, grid):
        self.cur.execute("SELECT * FROM courses WHERE grid = {}".format(grid))
        return self.cur.fetchall()

    def getPlayer(self, pid):
        self.cur.execute("SELECT * FROM users WHERE pid = {}".format(pid))
        return self.cur.fetchone()

    def getGame(self, gid):
        self.cur.execute("SELECT * FROM games WHERE gid = {}".format(gid))
        return self.cur.fetchone()

    def getCourse(self, cid):
        self.cur.execute("SELECT * FROM courses WHERE cid = {}".format(cid))
        return self.cur.fetchone()

    def putGame(self, pids, scores, cid, grid):
        self.cur.execute(
            "INSERT INTO games (cid, time, grid) VALUES({}, {}, {})".format(
                cid, int(time.time()), grid))
        self.cur.execute("SELECT LAST_INSERT_ID()")
        gid = self.cur.fetchone()[0]
        for x in range(len(pids)):
            self.cur.execute(
                "INSERT INTO player_game(pid, gid, scores) VALUES({}, {}, '{}')"
                    .format(pids[x], gid, json.dumps(scores[x])))
        self.conn.commit()

    def putCourse(self, pars, name, grid):
        cur.execute('INSERT INTO courses(pars, name, grid) VALUES("{}",{}, {})'
                .format(json.dumps(pars), name, grid))
        self.conn.commit()

