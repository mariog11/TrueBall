""" https://trueskill.org """

import Parser
import Ranking

filepath = 'MLB_2018.txt'

fp = open(filepath)

day = 0

for i in range(0, 150):
    day = Parser.getNextDay(fp)
    Ranking.addEntry(day)

Ranking.printTeamRanks()
games = Parser.getNextDay(fp)
Ranking.predictOutcomesByRating(games)
