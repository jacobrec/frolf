import pymysql as mdb
import sql


def setup():
    (username, pw, database) = sql.loginInfo()
    try:
        conn = mdb.connect(user=username, password=pw, db=database)
        return conn
    except mdb.err.OperationalError:
        print("Incorrect username, password, database combo")


def reset(cursor):
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS games')
    cursor.execute('DROP TABLE IF EXISTS groups')
    cursor.execute('DROP TABLE IF EXISTS courses')
    cursor.execute('DROP TABLE IF EXISTS player_game')


def init(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    pid INT NOT NULL AUTO_INCREMENT,
    name CHAR(50) NOT NULL,
    grid INT NOT NULL,
    PRIMARY KEY (pid)) """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS games (
    gid INT NOT NULL AUTO_INCREMENT,
    grid INT NOT NULL,
    cid INT NOT NULL,
    time INT NOT NULL,
    PRIMARY KEY (gid)) """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS groups (
    grid INT NOT NULL AUTO_INCREMENT,
    name CHAR(50) NOT NULL,
    passcode CHAR(50) NOT NULL,
    PRIMARY KEY (grid)) """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS player_game (
    pid INT NOT NULL,
    gid INT NOT NULL,
    scores CHAR(128) NOT NULL) """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS courses (
    cid INT NOT NULL AUTO_INCREMENT,
    pars CHAR(128) NOT NULL,
    name CHAR(50) NOT NULL,
    grid INT NOT NULL,
    PRIMARY KEY (cid))""")


def newServer():
    conn = setup()

    reset(conn.cursor())
    conn.commit()

    init(conn.cursor())
    conn.commit()

    conn.close()
    print("New database created")


def testData():
    conn = setup()
    cur = conn.cursor()
    cur.execute('INSERT INTO groups (name, passcode) VALUES("Test", "password")')
    cur.execute(
        'INSERT INTO groups (name, passcode) VALUES("Test2", "password")')
    cur.execute(
        'INSERT INTO courses(pars, name, grid) VALUES("[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4]","Rundle", 1)')
    cur.execute(
        'INSERT INTO courses(pars, name, grid) VALUES("[3, 3, 3, 3, 3, 3, 4, 3, 3]","Leduc", 1)')
    cur.execute(
        'INSERT INTO users(name, grid) VALUES("Testy McTestface", 1), ("Testy McTesterson", 1), ("Testa Testera", 1)')
    cur.execute(
        'INSERT INTO users(name, grid) VALUES("Testy2 McTestface", 2), ("Testy2 McTesterson", 2), ("Testa2 Testera", 2)')

    cur.execute(
        'INSERT INTO games (gid, grid, cid, time) VALUES(1, 1, 1, 1524844913), (2, 1, 1, 1524846356)')
    cur.execute(
        'INSERT INTO player_game (pid, gid, scores) VALUES (1, 1, "[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4]"), (1, 2, "[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,10]"), (2, 1, "[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,3]"), (2, 2, "[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,5]")')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    newServer()
    testData()
