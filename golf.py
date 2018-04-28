import json

def handicap(scores, pars):
    # TODO: make this an actual handicap function
    return sum([sum(x) for x in scores]) - sum([sum(x) for x in pars])


def getHandicap(pid, db):
    games = db.getAllGamesByPlayer(pid)  # cid, time, scores, gid, pars
    hc = handicap([json.loads(x[2]) for x in games], [
        json.loads(x[4]) for x in games])
    return hc
