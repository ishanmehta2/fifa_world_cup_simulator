import numpy as np
from scipy import stats
import math
import random
from collections import OrderedDict

N_SIMULATIONS = 400

win_prob = {'Netherlands': 0 / N_SIMULATIONS, 'Senegal': 0 / N_SIMULATIONS, 'Ecuador': 0 / N_SIMULATIONS,
            'Qatar': 0 / N_SIMULATIONS, 'United States': 0 / N_SIMULATIONS, 'Wales': 0 / N_SIMULATIONS, 'England': 0 / N_SIMULATIONS,
          'Iran': 0 / N_SIMULATIONS, 'Argentina': 0 / N_SIMULATIONS, 'Poland': 0 / N_SIMULATIONS, 'Mexico': 0 / N_SIMULATIONS,
            'Saudi Arabia': 0 / N_SIMULATIONS, 'France': 0 / N_SIMULATIONS, 'Australia': 0 / N_SIMULATIONS,
          'Tunisia': 0 / N_SIMULATIONS, 'Denmark': 0 / N_SIMULATIONS, 'Spain': 0 / N_SIMULATIONS, 'Japan': 0 / N_SIMULATIONS,
            'Costa Rica': 0 / N_SIMULATIONS, 'Germany': 0 / N_SIMULATIONS, 'Croatia': 0 / N_SIMULATIONS,
          'Morocco': 0 / N_SIMULATIONS, 'Belgium': 0 / N_SIMULATIONS, 'Canada': 0 / N_SIMULATIONS, 'Brazil': 0 / N_SIMULATIONS,
            'Switzerland': 0 / N_SIMULATIONS, 'Cameroon': 0 / N_SIMULATIONS, 'Serbia': 0 / N_SIMULATIONS,
          'Portugal': 0 / N_SIMULATIONS, 'Ghana': 0 / N_SIMULATIONS, 'Uruguay': 0 / N_SIMULATIONS, 'South Korea': 0 / N_SIMULATIONS}

points = {'Netherlands': 0, 'Senegal': 0, 'Ecuador': 0, 'Qatar': 0, 'United States': 0, 'Wales': 0, 'England': 0,
          'Iran': 0, 'Argentina': 0, 'Poland': 0, 'Mexico': 0, 'Saudi Arabia': 0, 'France': 0, 'Australia': 0,
          'Tunisia': 0, 'Denmark': 0, 'Spain': 0, 'Japan': 0, 'Costa Rica': 0, 'Germany': 0, 'Croatia': 0,
          'Morocco': 0, 'Belgium': 0, 'Canada': 0, 'Brazil': 0, 'Switzerland': 0, 'Cameroon': 0, 'Serbia': 0,
          'Portugal': 0, 'Ghana': 0, 'Uruguay': 0, 'South Korea': 0}

group_stage_1 = {'Qatar': 'Ecuador', 'England': 'Iran', 'Senegal': 'Netherlands', 'United States' : 'Wales',
               'Argentina': 'Saudi Arabia', 'Denmark' : 'Tunisia', 'Mexico' : 'Poland', 'France' : 'Australia',
               'Morocco': 'Croatia', 'Germany' : 'Japan', 'Spain' : 'Costa Rica', 'Belgium' : 'Canada',
               'Switzerland' : 'Cameroon', 'Uruguay' : 'South Korea', 'Portugal' : 'Ghana', 'Brazil' : 'Serbia'}

group_stage_2 = {'Wales': 'Iran', 'Qatar' : 'Senegal', 'Netherlands': 'Ecuador', 'England' : 'United States',
                 'Tunisia': 'Australia', 'Poland': 'Saudi Arabia', 'France' : 'Denmark', 'Argentina': 'Mexico',
                 'Japan': 'Costa Rica', 'Belgium' : 'Morocco', 'Croatia': 'Canada', 'Spain' : 'Germany',
                 'Cameroon': 'Serbia', 'South Korea' : 'Ghana', 'Brazil' : 'Switzerland', 'Portugal': 'Ghana'}

group_stage_3 = {'Ecuador' : 'Senegal', 'Netherlands': 'Qatar', 'Iran' : 'United States', 'Wales' : 'England',
                 'Tunisia' : 'France', 'Australia' : 'Denmark', 'Poland' : 'Argentina', 'Saudi Arabia':
                 'Mexico', 'Croatia' : 'Belgium', 'Canada' : 'Morocco', 'Japan' : 'Spain', 'Costa Rica' :
                 'Germany', 'South Korea' : 'Portugal', 'Ghana' : 'Uruguay', 'Serbia' : 'Switzerland',
                 'Cameroon': 'Brazil'}

group_A = ['Netherlands', 'Senegal', 'Ecuador', 'Qatar']
group_B = ['United States', 'Wales', 'England', 'Iran']
group_C = ['Argentina', 'Mexico', 'Poland', 'Saudi Arabia']
group_D = ['France', 'Australia', 'Tunisia', 'Denmark']
group_E = ['Spain', 'Japan', 'Costa Rica', 'Germany']
group_F = ['Croatia', 'Belgium', 'Morocco', 'Canada']
group_G = ['Brazil', 'Switzerland', 'Cameroon', 'Serbia']
group_H = ['Portugal', 'Ghana', 'South Korea', 'Uruguay']

groups = [group_A, group_B, group_C, group_D, group_E, group_F, group_G, group_H]

group_stages = [group_stage_1, group_stage_2, group_stage_3]


def populate_dict(dict, data):
    for row in data:
        if (row[0] != ''):
            team = row[0]
            dict[team] = row[1]
    return dict

def create_standings_dict(group, points):
    standings = {}
    for team in group:
        standings[team] = points[team]
    standings = sorted(standings.items(), key=lambda item: item[1])
    teams = []
    for key in standings:
        teams.append(key)
    first = teams[3][0]
    second = teams[2][0]
    return first, second

def round_of_16(list):
    ordered = {}
    ordered[list[0][0]] = list[1][1]
    ordered[list[0][1]] = list[1][0]
    ordered[list[2][0]] = list[3][1]
    ordered[list[2][1]] = list[3][0]
    ordered[list[4][0]] = list[5][1]
    ordered[list[4][1]] = list[5][0]
    ordered[list[6][0]] = list[7][1]
    ordered[list[6][1]] = list[7][0]
    return ordered


def quarterfinals(list):
    ordered = {}
    ordered[list[0]] = list[2]
    ordered[list[1]] = list[3]
    ordered[list[4]] = list[6]
    ordered[list[5]] = list[7]
    return ordered

def semifinals(list):
    ordered = {}
    ordered[list[0]] = list[1]
    ordered[list[2]] = list[3]
    return ordered

def finals(list):
    ordered = {}
    ordered[list[0]] = list[1]
    return ordered

def compare_elos(team1, team2, dict):
    elo_1 = dict[team1]
    elo_2 = dict[team2]
    mean = float(elo_1) - float(elo_2)
    var = 100000
    x = stats.norm(mean, math.sqrt(var))
    prob = (1 - x.cdf(0))
    if (prob > 0.5):
        return team1, prob
    elif(prob < 0.5):
        return team2, prob
    else:
        return "tie", prob

def single_game(prob, team1, team2):
    result = random.uniform(0 , 1)
    if (result < 0.6 * prob): #team 1 win
        return team1, team2
    elif (0.75 * prob < result < 1.4 * prob): #draw
        return 'draw'
    else: #team 2 win
        return team2, team1

def single_game_playoffs(prob, team1, team2): #cannot draw
    result = random.uniform(0, 1)
    if (result < prob):
        return team1
    else:
        return team2


def change_elos(dict, winner, loser):
    elo_1 = dict[winner]
    elo_2 = dict[loser]
    diff = float(elo_1) - float(elo_2)
    if (diff > 0): #expected winner wins
        dict[winner] = diff * 0.1 + float(elo_1)
        dict[loser] = float(elo_2) - diff * 0.05
    else: #expected winner loses
        dict[winner] = float(elo_1) - (abs(diff) * -0.5)
        dict[loser] = float(elo_2) + abs(diff) * 0.5
    return dict

def main():
    user = input("For which team do you want to get the probability of?  Type all for full list     ")
    for i in range(N_SIMULATIONS):
        points = {'Netherlands': 0, 'Senegal': 0, 'Ecuador': 0, 'Qatar': 0, 'United States': 0, 'Wales': 0,
                  'England': 0,
                  'Iran': 0, 'Argentina': 0, 'Poland': 0, 'Mexico': 0, 'Saudi Arabia': 0, 'France': 0, 'Australia': 0,
                  'Tunisia': 0, 'Denmark': 0, 'Spain': 0, 'Japan': 0, 'Costa Rica': 0, 'Germany': 0, 'Croatia': 0,
                  'Morocco': 0, 'Belgium': 0, 'Canada': 0, 'Brazil': 0, 'Switzerland': 0, 'Cameroon': 0, 'Serbia': 0,
                  'Portugal': 0, 'Ghana': 0, 'Uruguay': 0, 'South Korea': 0}
        data = np.genfromtxt('109Final.csv', delimiter=',', dtype='str') #load in data
        teams = {}
        populate_dict(teams, data) #put all data into a dictionary
        for group_stage in group_stages: #go through all group stages
            for entry in group_stage:
                team_1 = entry
                team_2 = group_stage[entry]
                higher = compare_elos(team_1, team_2, teams)
                prob = higher[1]
                ranking = single_game(prob, team_1, team_2)
                if (ranking != 'draw'):
                    winner = ranking[0]
                    points[winner] += 3 #add points as necessary
                    loser = ranking[1]
                    teams = change_elos(teams, winner, loser)
                else:
                    points[team_1] += 1
                    points[team_2] += 1
        advanced = []
        for group in groups:
            advancers = create_standings_dict(group, points) #create a sorted list of those who advanced
            advanced.append(advancers)
        ordered = round_of_16(advanced)
        quarters = []
        for game in ordered: # loop through round of 16
            team_1 = game
            team_2 = ordered[game]
            higher = compare_elos(team_1, team_2, teams)
            prob = higher[1]
            ranking = single_game_playoffs(prob, team_1, team_2)
            quarters.append(ranking)
        quarter_list = quarterfinals(quarters)
        semis = []
        for game in quarter_list: #loop through quarterfinals
            team_1 = game
            team_2 = quarter_list[game]
            higher = compare_elos(team_1, team_2, teams)
            prob = higher[1]
            ranking = single_game_playoffs(prob, team_1, team_2)
            semis.append(ranking)
        semi_list = semifinals(semis)
        final_teams = []
        for game in semi_list: #loop through semifinals
            team_1 = game
            team_2 = semi_list[game]
            higher = compare_elos(team_1, team_2, teams)
            prob = higher[1]
            ranking = single_game_playoffs(prob, team_1, team_2)
            final_teams.append(ranking)
        final_list = finals(final_teams)
        for game in final_list: #loop through finals
            team_1 = game
            team_2 = final_list[game]
            higher = compare_elos(team_1, team_2, teams)
            prob = higher[1]
            winner = single_game_playoffs(prob, team_1, team_2)
        win_prob[winner] += 1
    if (user == 'All'): #user wanted all probabilities
        for team in win_prob:
            win_prob[team] /= N_SIMULATIONS
        print(win_prob)
    else: #user wanted a specific team
        total_wins = win_prob[user]
        prob = total_wins / N_SIMULATIONS
        print(user + " has a" +  " " + str(prob) + " "  +"chance of winning the World Cup")

if __name__ == '__main__':
    main()


