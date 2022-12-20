import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

# ------------------------------------------------------------------------------------------
# Import raw data

import_data = pd.read_csv(r'Fifa_world_cup_matches.csv')
import_extra_data = pd.read_csv(r'extra_data.csv')
csv_main_dataframe = pd.DataFrame(import_data)
csv_extra_dataframe = pd.DataFrame(import_extra_data)

country_stats = {'country name' : [], 'average possession': [], 'total goals': [], 'total passes': [], 'total shots': [], 'total shots on target': []}
for i in csv_extra_dataframe.index:
    avg_possession = 0
    total_goals = 0
    total_passes = 0
    total_shots = 0
    total_shots_on_target = 0
    game_count = 0
    team_name = csv_extra_dataframe['Country'][i]

    for j in csv_main_dataframe.index:
        first_team_name = csv_main_dataframe['team1'][j]
        second_team_name = csv_main_dataframe['team2'][j]

        if first_team_name == team_name:
            game_count += 1
            avg_possession += csv_main_dataframe['possession team1'][j]
            total_goals += csv_main_dataframe['number of goals team1'][j]
            total_passes += csv_main_dataframe['passes completed team1'][j]
            total_shots += csv_main_dataframe['total attempts team1'][j]
            total_shots_on_target += csv_main_dataframe['on target attempts team1'][j]
        
        if second_team_name == team_name:
            game_count += 1
            avg_possession += csv_main_dataframe['possession team2'][j]
            total_goals += csv_main_dataframe['number of goals team2'][j]
            total_passes += csv_main_dataframe['passes completed team2'][j]
            total_shots += csv_main_dataframe['total attempts team2'][j]
            total_shots_on_target += csv_main_dataframe['on target attempts team2'][j]

    total_avg_possession = (avg_possession*100)/game_count
    country_stats['country name'].append(team_name)
    country_stats['average possession'].append(total_avg_possession)
    country_stats['total goals'].append(total_goals)
    country_stats['total passes'].append(total_passes)
    country_stats['total shots'].append(total_shots)
    country_stats['total shots on target'].append(total_shots_on_target)

country_stats_dataframe = pd.DataFrame(country_stats)

# ------------------------------------------------------------------------------------------
# App Layout
app.layout = html.Div([

    html.H1("World Cup 2022", style={'text-align': 'center'}),

    dcc.Dropdown(id='slct_country', options=[
        {'label': 'Argentina', 'value': 'ARGENTINA'},
        {'label': 'France', 'value': 'FRANCE'},
        {'label': 'Croatia', 'value': 'CROATIA'},
        {'label': 'Morocco', 'value': 'MOROCCO'},
        {'label': 'Netherlands', 'value': 'NETHERLANDS'},
        {'label': 'England', 'value': 'ENGLAND'},
        {'label': 'Brazil', 'value': 'BRAZIL'},
        {'label': 'Portugal', 'value': 'PORTUGAL'},
        {'label': 'Japan', 'value': 'JAPAN'},
        {'label': 'Senegal', 'value': 'SENEGAL'},
        {'label': 'Australia', 'value': 'AUSTRALIA'},
        {'label': 'Switzerland', 'value': 'SWITZERLAND'},
        {'label': 'Spain', 'value': 'SPAIN'},
        {'label': 'USA', 'value': 'UNITED STATES'},
        {'label': 'Poland', 'value': 'POLAND'},
        {'label': 'South Korea', 'value': 'SOUTH KOREA'},
        {'label': 'Germany', 'value': 'GERMANY'},
        {'label': 'Ecuador', 'value': 'ECUADOR'},
        {'label': 'Cameroon', 'value': 'CAMEROON'},
        {'label': 'Uruguay', 'value': 'URUGUAY'},
        {'label': 'Tunisia', 'value': 'TUNISIA'},
        {'label': 'Mexico', 'value': 'MEXICO'},
        {'label': 'Belgium', 'value': 'BELGIUM'},
        {'label': 'Ghana', 'value': 'GHANA'},
        {'label': 'Saudi Arabia', 'value': 'SAUDI ARABIA'},
        {'label': 'Iran', 'value': 'IRAN'},
        {'label': 'Costa Rica', 'value': 'COSTA RICA'},
        {'label': 'Denmark', 'value': 'DENMARK'},
        {'label': 'Serbia', 'value': 'SERBIA'},
        {'label': 'Wales', 'value': 'WALES'},
        {'label': 'Canada', 'value': 'CANADA'},
        {'label': 'Qatar', 'value': 'QATAR'},
    ])
])




# ------------------------------------------------------------------------------------------
# Connect Plotly Graph to Dash components

fig = px.bar(country_stats_dataframe, x='average possession', y='country name', orientation='h')
fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig.show()