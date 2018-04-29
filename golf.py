import json
import math


def handicap(scores, pars):
    """
    >>> handicap([[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4], [3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,9]], [[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4],[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4]])
    0

    >>> handicap([[4,3,3,3,3,3,4,4,3,3,3,3,3,3,3,3,3,4], [4,4,3,9,3,9,4,3,9,3,3,9,3,9,3,3,3,9]], [[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4],[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4]])
    2

    >>> handicap([[4,3,3,3,3,3,4,4,3,3,3,3,3,3,3,3,3,4], [4,4,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,9]], [[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4],[3,3,3,3,3,3,4,3,3,3,3,3,3,3,3,3,3,4]])
    2
    """
    if len(pars) == 0:
        return 0
    num = math.ceil(len(scores) / 2)
    both = [{"s": scores[i], "p":pars[i]} for i in range(len(pars))]
    both = sorted(both, key=lambda x: sum(x["s"]) - sum(x["p"]))[:num]

    tmpHandi = 0
    for x in both:
        tmpHandi += sum(x["s"]) - sum(x["p"])
    tmpHandi /= num


    handi = 0
    for x in both:
        handi += sum(eq_stroke_cont(x["s"], x["p"], tmpHandi))
    handi /= num

    return round(handi)


def eq_stroke_cont(score, par, handi):
    """
        Calculates the strokes with equitable stroke control procedures
    """
    diff = [score[i] - par[i] for i in range(len(par))]
    m = math.ceil(abs(handi) / 10) + 5
    return [min(m, diff[i]) for i in range(len(par))]


def getHandicap(pid, db):
    games = list(db.getAllGamesByPlayer(pid))  # cid, time, scores, gid, pars
    games.sort(key=lambda x: x[1], reverse=True)
    games = games[:20]
    hc = handicap([json.loads(x[2]) for x in games], [
        json.loads(x[4]) for x in games])
    return hc


if __name__ == "__main__":
    import doctest
    doctest.testmod()
