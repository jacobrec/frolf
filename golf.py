def handicap(scores, pars):
    # TODO: make this an actual handicap function
    return  sum([sum(x) for x in scores])- sum([sum(x) for x in pars])

