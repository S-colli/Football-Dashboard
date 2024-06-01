import pandas as pd

appearances = pd.read_csv(r'C:\Users\samue\Documents\00 Coding\Football Project\inputs\appearances.csv')
games = pd.read_csv(r'C:\Users\samue\Documents\00 Coding\Football Project\inputs\games.csv')
players = pd.read_csv(r'C:\Users\samue\Documents\00 Coding\Football Project\inputs\players.csv')
clubs = pd.read_csv(r'C:\Users\samue\Documents\00 Coding\Football Project\inputs\clubs.csv')
club_games = pd.read_csv(r'C:\Users\samue\Documents\00 Coding\Football Project\inputs\club_games.csv')

print(appearances.info())

print(appearances.nunique())

print(appearances.describe().apply(lambda s: s.apply('{0:.5f}'.format)))

appearances_df = appearances[appearances['player_current_club_id'] != -1]

print(games.info())

games_df = games.drop(columns = ['home_club_manager_name',
                                 'away_club_manager_name',
                                 'stadium',
                                 'attendance',
                                 'referee',
                                 'url',
                                 'home_club_formation',
                                 'away_club_formation',
                                 'aggregate',
                                 'competition_type'])
print(games_df.head())

unique_competition_ids = appearances['competition_id'].unique()
print(unique_competition_ids)

desired_competition_ids = ['ES1', 'FR1', 'IT1', 'NL1', 'PO1', 'GB1', 'L1']
appearances_df = appearances_df[appearances_df['competition_id'].isin(desired_competition_ids)]
games_df = games_df[games_df['competition_id'].isin(desired_competition_ids)]

appearances_df['goal_contributions'] = appearances_df['goals'] + appearances_df['assists']
print(appearances_df.head())

games_df['season'] = games_df['season'].astype(str)
games_df['season'] = games_df['season'] + '-' + (games_df['season'].astype(int) + 1).astype(str)
print(games_df.head())

home_games_df = games_df[['game_id',
                          'competition_id',
                          'season',
                          'round',
                          'date',
                          'home_club_id',
                          'home_club_goals',
                          'home_club_position',
                          'away_club_goals',
                          'home_club_name',
                          'away_club_name']].copy()

home_games_df.rename(columns = {'home_club_id' : 'club_id',
                                'home_club_goals' : 'goals_scored',
                                'home_club_position' : 'league_position',
                                'away_club_goals' : 'goals_conceded',
                                'home_club_name' : 'club_name',
                                'away_club_name' : 'opponent_name'}, inplace = True)

home_games_df['result'] = np.where(home_games_df['goals_scored'] > home_games_df['goals_conceded'], 'win',
                                   np.where(home_games_df['goals_scored'] < home_games_df['goals_conceded'], 'loss',
                                            'draw'))

home_games_df['at_home'] = True

print(home_games_df.head())

away_games_df = games_df[['game_id',
                          'competition_id',
                          'season',
                          'round',
                          'date',
                          'away_club_id',
                          'away_club_position',
                          'home_club_goals',
                          'away_club_goals',
                          'home_club_name',
                          'away_club_name']].copy()

away_games_df.rename(columns = {'away_club_id' : 'club_id',
                                'away_club_position' : 'league_position',
                                'home_club_goals' : 'goals_conceded',
                                'away_club_goals' : 'goals_scored',
                                'home_club_name' : 'opponent_name',
                                'away_club_name' : 'club_name'}, inplace = True)

away_games_df['result'] = np.where(away_games_df['goals_scored'] > away_games_df['goals_conceded'], 'win',
                                   np.where(away_games_df['goals_scored'] < away_games_df['goals_conceded'], 'loss',
                                            'draw'))

away_games_df['at_home'] = False

print(away_games_df.head())

games_long_df = pd.concat([home_games_df, away_games_df], ignore_index = True)

unique_rounds = games_long_df['round'].unique()
print(unique_rounds)

games_long_df['round'] = games_long_df['round'].str.replace('. Matchday', '', case = False)

games_long_df['league_position'] = games_long_df['league_position'].astype(int)
games_long_df['round'] = games_long_df['round'].astype(int)
games_long_df['at_home'] = games_long_df['at_home'].astype(bool)

games_long_df = games_long_df.sort_values(by = 'game_id').reset_index(drop = True)

print(games_long_df.info())

players_df = players[['player_id',
                      'country_of_citizenship',
                      'date_of_birth',
                      'sub_position',
                      'position',
                      'foot',
                      'height_in_cm',
                      'image_url',
                      'market_value_in_eur']].copy()

players_df.rename(columns = {'country_of_citizenship' : 'nationality'}, inplace = True)

print(players_df.head())

appearances_df.to_csv(r'C:\Users\samue\Documents\00 Coding\Football Project\outputs\appearances_df.csv', index = False)
games_long_df.to_csv(r'C:\Users\samue\Documents\00 Coding\Football Project\outputs\games_long_df.csv', index = False)
players_df.to_csv(r'C:\Users\samue\Documents\00 Coding\Football Project\outputs\players_df.csv', index = False)
