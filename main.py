import pandas as pd
import unicodedata


def __load_team_data(game_file, team):
    """Loads boxscore and players information in gane_file for required team"""

    # loads team information
    df_t = pd.read_excel(game_file, sheet_name='{}_team'.format(team))

    # identify main position for each player
    df_t['POS'] = [x.split('-')[0] for x in df_t['POS']]

    # drop not required columns
    df_t = df_t[['PLAYER', 'POS']]

    # loads box score
    df_bs = pd.read_excel(game_file, sheet_name='{}_boxscore'.format(team))

    # fix player name issue: heading and last character for initial players
    df_bs['PLAYER'] = [unicodedata.normalize("NFKD", x.replace('undefined Headshot', ''))
                       for x in df_bs['PLAYER']]
    df_bs['PLAYER'] = [x[:-1] if k < 5 else x for k, x in enumerate(df_bs['PLAYER'])]

    # merge DataFrame
    df_bs = pd.merge(df_bs, df_t, how="inner", left_on='PLAYER', right_on='PLAYER')

    # insert column with team name
    df_bs['TEAM'] = team

    return df_bs


def load_datasets(game_file, teams):
    """Loads DataFrame with data for each team in dataset
    Returns DataFrame with data for each team"""
    out = []
    for t in teams:
        df_t = __load_team_data(game_file, t)
        out.append(df_t)

    # concat DataFrames
    df = pd.concat(out)
    return df


def dataset_preprocessing(df):
    """ Prepares dataset for sunburst creation
    - drop not needed columns
    - filter players with no points
    - Create attribute with points from 3 points shots
    - Create attribute PTS_3 with points not from 3 points shots
    - Create attribute PTS_not3 with total points in same player position
    - melts table to create different rows in PTS_3 and PTS_not3
    """

    # drop columns and filter only players with annotation
    df = df[['PLAYER', '3PM', 'PTS', 'POS', 'TEAM']]
    df = df[df['PTS'] > 0]

    # separate 3p from other PTS
    df['PTS_3'] = 3 * df['3PM']
    df['PTS_not3'] = df['PTS'] - df['PTS_3']

    # add column with the sum of points in position
    pt_pos = df.pivot_table(index=['TEAM', 'POS'], aggfunc={'PTS': 'sum'})
    pt_pos = pt_pos.rename(columns={'PTS': 'POS_PTS'})
    df = pd.merge(df, pt_pos, left_on=['TEAM', 'POS'], right_index=True)

    # transform format of table
    df = pd.melt(df, id_vars=['TEAM', 'POS', 'PLAYER', 'PTS', 'POS_PTS'],
                 value_vars=['PTS_3', 'PTS_not3'])
    df = df[df['value'] > 0]

    # rename values with text to be shown in sunburst
    df['variable'] = df['variable'].map({'PTS_3': '3P', 'PTS_not3': '-'})
    df['TEAM'] = df['TEAM'].map({'TOR': 'Raptors', 'IND': 'Pacers'})
    df['POS'] = df['POS'].map({'F': 'Forward', 'C': 'Center', 'G': 'Guard'})

    return df


def create_sunburst_pivot_table(df):
    """Transform data to pivot table in format for sunburst plot.
    It sorts the data to create sorted view in the sunburst"""
    pt = df.pivot_table(index=['TEAM', 'POS', 'PLAYER', 'variable'],
                        aggfunc={'PTS': 'mean', 'value': 'mean', 'POS_PTS': 'mean'})
    pt['TEAM_c'] = [x[0] for x in pt.index]
    pt['POS_c'] = [x[1] for x in pt.index]
    pt['PLAYER_c'] = [x[2] for x in pt.index]
    pt = pt.sort_values(by=['TEAM_c', 'POS_PTS', 'PTS'], ascending=[False, False, False])

    # drop columns
    pt = pt['value']
    return pt


def save_sunburst_data_infogram_format(data, out_file):
    """Save sunburst data to .csv in the format required by infogram for sunburst object"""
    with open(out_file, 'w') as f:
        # write header
        f.write(','.join(data.index.names))
        f.write('\n')
        # write lines
        last_idx = None
        for idx in data.index:
            pass_all_idx = False
            if last_idx is None:
                new_idx = idx
            else:
                new_idx = []
                for k in range(len(idx)):
                    if idx[k] == last_idx[k] and not pass_all_idx:
                        new_idx.append('')
                    else:
                        new_idx.append(idx[k])
                        pass_all_idx = True
                new_idx = tuple(new_idx)

            last_idx = idx
            f.write(','.join(list(new_idx) + ['{:0.0f}'.format(data[idx])]))
            f.write('\n')

        f.close()

    return


# main code
game_file = r'dataset\NBA_game_data.xlsx'
out_infogram_file = r'dataset\game_scorebox.csv'

teams = ['TOR', 'IND']

# load DataFrames
df = load_datasets(game_file, teams)

# data preprocessing
df = dataset_preprocessing(df)

# create data for sunburst
sunburst_data = create_sunburst_pivot_table(df)

# save data to file
save_sunburst_data_infogram_format(sunburst_data, out_infogram_file)
