""" https://trueskill.org """

import Parser
import Ranking
import matplotlib.pyplot as mpl

# filepath = 'MLB_2017.txt' # 205
filepath = 'MLB_2018.txt' # 183


fp = open(filepath)


total_count = 0
total_correct = 0
average_points = []
discrete_points = []
middle_points = [] # for drawing a line at the 0.5 level
x_values = []
labels = ["Daily ratio of successful guesses", "Average ratio of successful guesses"]
starting_day = 20
for i in range(0, 100):
    day = Parser.getNextDay(fp)
    middle_points.append(0.5)
    if i > starting_day:
        correct, count = Ranking.predictOutcomesByProbability(day)
        total_correct = total_correct + correct
        total_count = total_count + count
        average_points.append(total_correct / total_count)
        discrete_points.append(correct / count)
        x_values.append(i)
        print(total_correct, "/", total_count, (total_correct / total_count))

    Ranking.addEntry(day)
    # Ranking.printHmAwayProb()



mpl.ylim([0.1, 0.9])
print(total_correct, "/", total_count, (total_correct/total_count))

mpl.plot(x_values, discrete_points)
mpl.plot(x_values, average_points)
mpl.legend(labels, loc='upper center', bbox_to_anchor=(0.5, -0.12), shadow=True, ncol=1)
# mpl.plot(x_values, middle_points)
mpl.ylabel('Probability of guessing correctly')
mpl.title('MLB 2018 Unique Home-Field Advantage')
mpl.xlabel('Day')

mpl.savefig("MLB 2018 Unique Home-Field Advantage", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches='tight', pad_inches=1,
        frameon=None, metadata=None)

# mpl.show()


# Ranking.printTeamRanks()
games = Parser.getNextDay(fp)
# Ranking.predictOutcomesByRating(games)
