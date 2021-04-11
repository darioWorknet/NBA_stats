import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def create_heat_array(df, teams):
    df = df.copy()
    home,visit,home_score,visit_score,total=df.columns
#     n_teams = df[home].nunique()
    n_teams = len(teams)
    square_array = np.zeros((n_teams,n_teams))
    # FOR REPETITIVE DATA, CALCULATE MEAN
    # print(df.head().to_string())
    # Calculate total score mean for identical games
    df['mean'] = df.groupby([df.columns[0],df.columns[1]]).TotalScore.transform('mean')
    # print(df.head().to_string())
    # Drop identical games
    df.drop_duplicates(subset=[df.columns[0], df.columns[1]], inplace=True)
    for index, row in df.iterrows():
        # Row values
        team_home = row[home]
        team_visit = row[visit]
        score_home = row[home_score]
        score_visit = row[visit_score]
        # Index for square array
        index_home = teams.index(team_visit)
        index_visit = teams.index(team_home)
        # Filling square array
        square_array[index_home,index_visit] = row['mean']
    # Discard 0 values, to add more precession while ploting
    square_array[square_array == 0] = np.nan
    return square_array 




def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts



# Returns an array containing every team without duplicates
def unique_teams(df):
    teams1 = df[df.columns[0]].unique()
    teams2 = df[df.columns[1]].unique()
    list1, list2 = list(teams1), list(teams2)
    diff = set(list2) - set(list1)
    teams = list(list1 + list(diff))
    # REturn flatten array
    return [t for t in teams]


def heatmap(df, ax=None,f_size=5,
            cbar_kw={}, cbarlabel="", **kwargs):
    plt.figure(figsize=(f_size,f_size), dpi=150)

    if not ax:
        ax = plt.gca()

    # List of teams
    teams = unique_teams(df)
    # Columns casting
    df[df.columns[2]] = df[df.columns[2]].astype(np.int64)
    df[df.columns[3]] = df[df.columns[3]].astype(np.int64)
        
    # Converting data
    data = create_heat_array(df, teams)
    # Plot the heatmap
    im = ax.imshow(data, **kwargs)
    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(teams)
    ax.set_yticklabels(teams)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")
    

    # Turn spines off and create white grid.
    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)
    
    # Annotations for each 'pixel'
#     texts = annotate_heatmap(im, valfmt="{x:.1f}")
    
#     plt.figure(figsize=(5,5))
    plt.savefig('output.png')
    
    return im, cbar