def handicap(scores, pars):
    return  sum([sum(x) for x in scores])- sum([sum(x) for x in pars])

