import pandas as pd
import numpy as np
import resources.df_helper as df_helper

# GLOBAL DF
global_df = None
unique_teams = None
below_dict = None
above_dict = None
total_dict = None

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


# AUXILIARY FUNCTIONS FOR FACTORS CALCULATIONS -----------
def get_factors(df, p=5):
    below = get_single_factor(df, p)
    above = get_single_factor(df, 100-p)
    total = total_games(df)
    return below, above, total

def total_games(df):
    teams_counter = df.iloc[:,[0,1]].values.tolist()
    # Flattening result
    teams_counter = [t for sub in teams_counter for t in sub]
    return factor_counter(teams_counter)
    
def get_single_factor(df, percentile):
    teams_cont = list()
    for team in unique_teams:
        df_ = df_helper.query_team(df, team)
        x = df_['TotalScore']
        
        p = np.percentile(x, percentile)
        
        if percentile < 50:
            teams_df = df_.loc[df_['TotalScore'] <= p]
        else:
            teams_df = df_.loc[df_['TotalScore'] >= p]
            
        teams = teams_df.iloc[:,[0,1]].values.tolist()
        # Flattening and filtering results
        teams = [t for sub in teams for t in sub if t != team]
        teams_cont.append(teams)
        
    teams_counter = [t for sub in teams_cont for t in sub]
    return factor_counter(teams_counter)

def factor_counter(teams_counter):
    return_dict = dict()
    for t in unique_teams:
        return_dict[t] = 0
    for t in teams_counter:
        return_dict[t] += 1
    return return_dict


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





def stats(df):

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
    below_dict, above_dict, total_dict = get_factors(df, 10)

    # factorDown
    df_['factorDown'] = df_.apply(factor_down, axis=1)
    # factorUp
    df_['factorUp'] = df_.apply(factor_up, axis=1)

    return df_