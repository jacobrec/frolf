import pymysql as mdb


def setup():
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

    init(cursor)


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
    print("New database created")

def testData(conn):
    cur = conn.cursor()
    cur.execute('INSERT INTO groups (name, passcode) VALUES("Frisbee", "password")')
    cur.execute('INSERT INTO courses(pars, name, grid) VALUES("[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4]","Rundle", 1)')
    cur.execute('INSERT INTO users(name, grid) VALUES("Jacob", 1), ("Ben", 1), ("Peter", 1), ("Isaac", 1), ("Graham", 1)')



if __name__ == "__main__":
    newServer()
