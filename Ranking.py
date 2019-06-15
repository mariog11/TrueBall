from trueskill import Rating, quality_1vs1, rate_1vs1
import trueskill
import itertools
import math

starting_rating = 25
alice, bob = Rating(25), Rating(30)  # assign Alice and Bob's ratings

teams = {}
teams_home_prob = {}
teams_away_prob = {}
teamNames = []


def addSingleEntry(team1, team2):
    if not teamNames.__contains__(team1[0]):
        teamNames.append(team1[0])
        teams[team1[0]] = [Rating()]
        teams_home_prob[team1[0]] = [0, 0]
        teams_away_prob[team1[0]] = [0, 0]

    if not teamNames.__contains__(team2[0]):
        teamNames.append(team2[0])
        teams[team2[0]] = [Rating()]
        teams_home_prob[team2[0]] = [0, 0]
        teams_away_prob[team2[0]] = [0, 0]

    if team1[1] > team2[1]:
        (new_r1,), (new_r2,) = trueskill.rate([teams[team1[0]], teams[team2[0]]], ranks=[0, 1])
        teams[team1[0]] = [new_r1]
        teams[team2[0]] = [new_r2]
        teams_home_prob[team2[0]] = [teams_home_prob[team2[0]][0], teams_home_prob[team2[0]][1] + 1]
        teams_away_prob[team1[0]] = [teams_away_prob[team1[0]][0] + 1, teams_away_prob[team1[0]][1] + 1]

    if team1[1] < team2[1]:
        (new_r1,), (new_r2,) = trueskill.rate([teams[team1[0]], teams[team2[0]]], ranks=[1, 0])
        teams[team1[0]] = [new_r1]
        teams[team2[0]] = [new_r2]
        teams_home_prob[team2[0]] = [teams_home_prob[team2[0]][0] + 1, teams_home_prob[team2[0]][1] + 1]
        teams_away_prob[team1[0]] = [teams_away_prob[team1[0]][0], teams_away_prob[team1[0]][1] + 1]

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
    correct_guesses = 0
    total_guesses = 0
    for game in games:
        team1 = game[0]
        team2 = game[1]

        total_guesses = total_guesses + 1

        # team2 has a record of 4 wins out of 6 home games
        # team2's home field advantage is (4/6) - 0.5
        #                               = 0.66 - 0.5
        #                               = 0.16
        # home_advantage = getHomeWinRatio()-0.5
        home_advantage = getHomeWinRatioTeam(team2)-0.5
        # home_advantage = 0

        # probability of team1 winning is their rating - team2's home field advantage
        prob = win_probability(teams[team1[0]], teams[team2[0]]) - home_advantage

        # print(team1[0], "has a", prob, "chance of beating", team2[0])
        if team1[1] > team2[1]:
            # print(team1[0], "beat", team2[0], team1[1], "to", team2[1])
            if float(prob) > 0.5:
                correct_guesses = correct_guesses + 1

        elif team1[1] < team2[1]:
            # print(team1[0], "lost to", team2[0], team1[1], "to", team2[1])
            if float(prob) < 0.5:
                correct_guesses = correct_guesses + 1

        elif team1[1] == team2[1]:
            # print(team1[0], "tied", team2[0], team1[1], "to", team2[1])
            if float(prob) == 0.5:
                correct_guesses = correct_guesses + 1

    return correct_guesses, total_guesses


def predictOutcomesByRating(games):
    for game in games:
        team1 = game[0]
        team2 = game[1]

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


def getHomeWinRatio():
    total_wins = 0
    total_games = 0

    for name in teamNames:
        total_wins = total_wins + teams_home_prob[name][0]
        total_games = total_games + teams_home_prob[name][1]

    return total_wins/total_games


def getAwayWinRatio():
    total_wins = 0
    total_games = 0

    for name in teamNames:
        total_wins = total_wins + teams_away_prob[name][0]
        total_games = total_games + teams_away_prob[name][1]

    return total_wins/total_games


def getAwayWinRatioTeam(team):
    if teams_home_prob[team[0]][1] == 0:
        return 0.5

    return teams_away_prob[team[0]][0]/teams_away_prob[team[0]][1]


def getHomeWinRatioTeam(team):
    if teams_home_prob[team[0]][1] == 0:
        return 0.5

    return teams_home_prob[team[0]][0] / teams_home_prob[team[0]][1]


def printTeamHomeProb():
    total_wins = 0
    total_games = 0
    for name in teamNames:
        total_wins = total_wins + teams_home_prob[name][0]
        total_games = total_games + teams_home_prob[name][1]
        print(name, "\t", teams_home_prob[name])

    print("[Home wins, Home Games] =", "{0:.2f}".format(total_wins/total_games))


def printTeamAwayProb():
    total_wins = 0
    total_games = 0
    for name in teamNames:
        total_wins = total_wins + teams_away_prob[name][0]
        total_games = total_games + teams_away_prob[name][1]
        print(name, "\t", teams_away_prob[name])

    print("[Away wins, Away Games] =", "{0:.2f}".format(total_wins / total_games))


def win_probability(team1, team2, home_advantage=0):
    delta_mu = sum(r.mu for r in team1) - (sum(r.mu for r in team2)+home_advantage)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (trueskill.BETA * trueskill.BETA) + sum_sigma)
    ts = trueskill.global_env()
    return ts.cdf(delta_mu / denom)



