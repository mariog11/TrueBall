from trueskill import Rating, quality_1vs1, rate_1vs1
import trueskill
import itertools
import math

starting_rating = 25
alice, bob = Rating(25), Rating(30)  # assign Alice and Bob's ratings

teams = {}
teamNames = []


def addSingleEntry(team1, team2):
    if team1[0] == "-" or team2[0] == "-":
        return

    if not teamNames.__contains__(team1[0]):
        teamNames.append(team1[0])
        teams[team1[0]] = [Rating()]

    if not teamNames.__contains__(team2[0]):
        teamNames.append(team2[0])
        teams[team2[0]] = [Rating()]

    if team1[1] > team2[1]:
        (new_r1,), (new_r2,) = trueskill.rate([teams[team1[0]], teams[team2[0]]], ranks=[0, 1])
        teams[team1[0]] = [new_r1]
        teams[team2[0]] = [new_r2]

    if team1[1] < team2[1]:
        (new_r1,), (new_r2,) = trueskill.rate([teams[team1[0]], teams[team2[0]]], ranks=[1, 0])
        teams[team1[0]] = [new_r1]
        teams[team2[0]] = [new_r2]

    if team1[1] == team2[1]:
        (new_r1,), (new_r2,) = trueskill.rate([teams[team1[0]], teams[team2[0]]], ranks=[0, 0])
        teams[team1[0]] = [new_r1]
        teams[team2[0]] = [new_r2]


def addEntry(games):
    for game in games:
        team1 = game[0]
        team2 = game[1]
        addSingleEntry(team1, team2)


def predictOutcomesByProbability(games):
    for game in games:
        team1 = game[0]
        team2 = game[1]
        if team1[0] != "-" and team1[0] != "-":
            prob = "{0:.2f}".format(win_probability(teams[team1[0]], teams[team2[0]]))
            print(team1[0], "has a", prob, "chance of beating", team2[0])
            if team1[1] > team2[1]:
                print(team1[0], "beat", team2[0], team1[1], "to", team2[1])

            if team1[1] < team2[1]:
                print(team1[0], "lost to", team2[0], team1[1], "to", team2[1])

            if team1[1] == team2[1]:
                print(team1[0], "tied", team2[0], team1[1], "to", team2[1])

        print("")


def predictOutcomesByRating(games):
    for game in games:
        team1 = game[0]
        team2 = game[1]
        if team1[0] != "-" and team1[0] != "-":
            r1 = getRating(team1)
            r2 = getRating(team2)
            print(team1[0], "[", r1, "]\t", team2[0], "[", r2, "]")

            if team1[1] > team2[1]:
                print(team1[0], "beat", team2[0], team1[1], "to", team2[1])

            if team1[1] < team2[1]:
                print(team1[0], "lost to", team2[0], team1[1], "to", team2[1])

            if team1[1] == team2[1]:
                print(team1[0], "tied", team2[0], team1[1], "to", team2[1])

        print("")


def getRating(team):
    return "{0:.2f}".format(teams[team[0]][0].mu)


def printTeamNames():
    for name in teamNames:
        print(name)


def printTeamRanks():
    for name in teamNames:
        print(name, "\t", teams[name])


def win_probability(team1, team2):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (trueskill.BETA * trueskill.BETA) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)



