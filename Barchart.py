import pandas as pd
import matplotlib.pyplot as plt


def barchart(df, team_analysis,y_range=[150,250]):
    x_teams = list()
    h_score = list()
    for index, row in df.iterrows():
        team1, team2, score1, score2 = row
        # Getting team
        if team1 != team_analysis:
            x_teams.append(team1)
        else:
            x_teams.append(team2)
        # Getting total score
        h_score.append(score1+score2)

    plt.xticks(rotation=90)
    plt.ylim(y_range)
    plt.bar(x_teams,h_score)
    plt.xlabel("Teams")
    plt.ylabel("Total score")
    plt.title("Team A matches")
    plt.show()

    # return x_teams, h_score



def barchart_order(df, team_analysis,y_range=[150,250]):

    # Sort by TotalScore
    df.sort_values(by=[df.columns[4]], inplace=True)
    
    x_teams = list()
    h_score = list()
    for index, row in df.iterrows():
        team1, team2, score1, score2, total_score = row
        print(total_score)
        # Getting team
        if team1 != team_analysis:
            x_teams.append(team1)
        else:
            x_teams.append(team2)
        # Getting total score
        h_score.append(total_score)

    plt.xticks(rotation=90)
    plt.ylim(y_range)
    plt.bar(x_teams,h_score)
    plt.xlabel("Teams")
    plt.ylabel("Total score")
    plt.title("Team A matches")
    plt.show()

    # return x_teams, h_score  