import pandas as pd
import numpy as np


# Returns an array containing every team without duplicates
def unique_teams(df):
    teams1 = df[df.columns[0]].unique()
    teams2 = df[df.columns[1]].unique()
    list1, list2 = list(teams1), list(teams2)
    diff = set(list2) - set(list1)
    teams = list(list1 + list(diff))
    # Return flatten array
    return [t for t in teams]


# This function allows to append a new row to the dataframe easily
def append_data(df, col1, col2, col3, col4):
    # Insert new row at the bottom
    df.loc[-1] = [col1, col2, np.int64(int(col3)), np.int64(int(col4))]
    # Reset indexes
    df.reset_index(drop=True, inplace=True)


def append_row(df, new_row):
    # Insert new row at the bottom
    df.loc[-1] = new_row
    # Reset indexes
    df.reset_index(drop=True, inplace=True)


# Returns new dataframe with all games for a team
def query_team(df, team):
    df_ = df.query("HomeTeam == '{0}' or AwayTeam == '{0}'".format(team))
    return df_