import pandas as pd
import numpy as np
import resources.df_helper as df_helper

# GLOBAL DF
global_df = None
unique_teams = None
below_dict = None
above_dict = None
total_dict = None
weighted_above_dict = None
weighted_below_dict = None

# MEAN ----------------------------------------------------
# Auxiliary function
def mean_team(df, team):
    df_ = df_helper.query_team(df, team)
    return df_['TotalScore'].mean()
# Mean for each row
def mean(row):
    team = row['team']
    new_row = mean_team(global_df, team)
    return new_row


# P25 -----------------------------------------------------
# Auxiliary function
def percentile_team(df, team, percentile):
    df_ = df_helper.query_team(df, team)
    x = df_["TotalScore"]
    p = np.percentile(x, percentile)
    return p
# Percentile 25 for each row
def percentile_25(row):
    team = row['team']
    new_row = percentile_team(global_df, team, 25)
    return new_row


# P75 -----------------------------------------------------
# Percentile 75 for each row
def percentile_75(row):
    team = row['team']
    new_row = percentile_team(global_df, team, 75)
    return new_row


# AUXILIARY FUNCTIONS FOR FACTORS CALCULATIONS __________________________________
def get_factors(df, p):
    below = get_single_factor(df, p)
    above = get_single_factor(df, 100-p)
    total = total_games(df)
    return below, above, total

def total_games(df):
    count_dict = dict()
    teams_counter = df.iloc[:,[0,1]].values.tolist()
    # Flattening result
    teams_counter = [t for sub in teams_counter for t in sub]
    # Count time each team appears in list
    return list_to_frecuency_dict(teams_counter)
    
def get_single_factor(df, percentile):
    list_of_dicts = list()
    for team in unique_teams:
        df_ = df_helper.query_team(df, team)
        x = df_['TotalScore']
        # Position of percentile for x dataset
        p = np.percentile(x, percentile)
        print("Team: {}, percentile: {}, pos: {}". format(team, percentile, p))
        # Filter df, only getting result out of percentile range
        percentile_df = filter_by_percentile(df_, percentile, p)
        # Create a frecuency dictionary from dataframe
        list_of_dicts.append(frecuencies_df(percentile_df, team))
    return sum_dicts(list_of_dicts)


def sum_dicts(dicts):
    sum_dict = {team:0 for team in unique_teams}
    for d in dicts:
        sum_dict = {key: sum_dict.get(key, 0) + d.get(key, 0) for key in set(sum_dict)}
    return sum_dict


def filter_by_percentile(df, percentile, p):
    if percentile < 50:
        return df.loc[df['TotalScore'] < p]
    else:
        return df.loc[df['TotalScore'] > p]


def frecuencies_df(df, team):
    f_dict = dict()
    for index, row in df.iterrows():
        team1, team2 = row[0], row[1]
        if team1 == team: # Get 'away team'
            team1 = team2
        f_dict[team1] = f_dict.get(team1, 0) + 1
    return f_dict
        


# Can not be used 'defaultdict' from collections. Because all items in unique_teams should be initialized
def list_to_frecuency_dict(lst):
    frecuency_dict = {team:0 for team in unique_teams}
    for l in lst:
        frecuency_dict[l] += 1
    return frecuency_dict



# FACTOR DOWN ---------------------------------------------
def factor_down(row):
    team = row['team']
    new_row = below_dict[team]/total_dict[team]*100
    return new_row


# FACTOR UP -----------------------------------------------
def factor_up(row):
    team = row['team']
    new_row = above_dict[team]/total_dict[team]*100
    return new_row



# AUXILARY FUNTIONS _______________________________________________________________
def get_weighted_factor(df, percentile=10):
    below = get_weighted_factors(df, percentile)
    above = get_weighted_factors(df, 100-percentile)
    return below, above

def get_weighted_factors(df, percentile):
    list_of_dicts = list()
    for team in unique_teams:
        df_ = df_helper.query_team(df, team)
        x = df_['TotalScore']
        # Position of percentile for x dataset
        p = np.percentile(x, percentile)
        opo_p = np.percentile(x, oposite_percentile(percentile))
        width = abs(p - opo_p)
        # Filter df, only getting result out of percentile range
        teams_df = filter_by_percentile(df_, percentile, p)
        # Create a frecuency dictionary from dataframe
        list_of_dicts.append(weights_df(teams_df, team, p, width))
    return sum_dicts(list_of_dicts)

def weights_df(df, team, p, w):
    f_dict = dict()
    for index, row in df.iterrows():
        team1, team2 = row[0], row[1]
        if team1 == team:
            team1 = team2
        x = row[4]
        # Calculating weight
        weight = get_weight(x, p, w)
        # Adding weight
        f_dict[team1] = f_dict.get(team1, 0) + weight
    return f_dict

def get_weight(x, p, w):
    return (x-p)*(x-p) / w

def oposite_percentile(percentile):
    return 50+(50-percentile)


# WEIGHTED FACTOR DOWN -------------------------------------
def weighted_factor_down(row):
    team = row['team']
    new_row = weighted_below_dict[team]/total_dict[team]*100
    return new_row

# WEIGHTED FACTOR UP -------------------------------------
def weighted_factor_up(row):
    team = row['team']
    new_row = weighted_above_dict[team]/total_dict[team]*100
    return new_row


def stats(df, p_factor=10, p_weight=15):

    global global_df
    global_df = df

    global unique_teams
    unique_teams = df_helper.unique_teams(df)
    df_ = pd.DataFrame(unique_teams, columns=['team'])

    # Calculating the mean for each team
    df_['mean'] = df_.apply(mean, axis=1)
    # P25
    df_['P25'] = df_.apply(percentile_25, axis=1)
    # P75
    df_['P75'] = df_.apply(percentile_75, axis=1)

    # Auxiliary data for lowFactor and upFactor
    global below_dict
    global above_dict
    global total_dict
    below_dict, above_dict, total_dict = get_factors(df, p_factor)

    # factorDown
    df_['factorDown'] = df_.apply(factor_down, axis=1)
    # factorUp
    df_['factorUp'] = df_.apply(factor_up, axis=1)


    # Auxiliary data for WEIGHTED lowFactor and upFactor
    global weighted_below_dict
    global weighted_above_dict
    weighted_below_dict, weighted_above_dict = get_weighted_factor(df, p_weight)

    # weightedFactorDown
    df_['WfactorDown'] = df_.apply(weighted_factor_down, axis=1)
    # weightedFactorUp
    df_['WfactorUp'] = df_.apply(weighted_factor_up, axis=1)

    return df_