days_of_the_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
standings = "Standings"


def getScore(team):
    left = team.find('(')
    right = team.find(')')
    score = team[left+1:right]
    return score


def getTeamName(team):
    left = team.find('(')
    name = team[:left-1]
    return name


def getGameData(line):
    mid = line.find('@')

    if mid == -1:
        return ("-", -1), ("-", -1)

    left = line[0:mid]
    right = line[mid+2:]

    score1, score2 = getScore(left), getScore(right)

    name1 = getTeamName(left)
    name2 = getTeamName(right)

    return (name1, score1), (name2, score2)


def getNextDay(fp):
    games = []
    line = fp.readline()

    if not line:
        return games

    while line:

        # if at new day
        for day in days_of_the_week:
            if line.__contains__(day):
                continue

        # if line has score data
        team1, team2 = getGameData(line)
        if team1[0] != "-" and team2[0] != "-":
            games.append((team1, team2))

        # if at end of week
        if line.__contains__(standings):
            break

        line = fp.readline()

    return games
