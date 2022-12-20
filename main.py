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

country_stats = {'country name' : [], 'country ranking': [], 'average possession': [], 'total goals': [], 'total passes': [], 'total shots': [], 'total shots on target': []}
for i in csv_extra_dataframe.index:
    avg_possession = 0
    total_goals = 0
    total_passes = 0
    total_shots = 0
    total_shots_on_target = 0
    game_count = 0
    team_name = csv_extra_dataframe['Country'][i]
    country_stats['country ranking'].append(i+1)

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
    dcc.Dropdown(id='slct_stat', options=[{'label': 'ranking', 'value': 'country ranking'},
        {'label': 'average possession', 'value': 'average possession'},
        {'label': 'total goals', 'value': 'total goals'},
        {'label': 'total passes', 'value': 'total passes'},
        {'label': 'total shots', 'value': 'total shots'},
        {'label': 'total shots on target', 'value': 'total shots on target'}],
        multi=False,
        value='country ranking',
        style={'width': "40%", 'height': '100%'},
        ),

    dcc.Graph(id='team_rankings', figure={}, style={'width': "40%", 'height': '100%'}, config={
        'displayModeBar': False
        }),
])

# ------------------------------------------------------------------------------------------
# Connect Plotly Graph to Dash components
@app.callback(
    Output(component_id='team_rankings', component_property='figure'),
    Input(component_id='slct_stat', component_property='value')
)
def update_graph(option_slctd):

    df_copy = country_stats_dataframe.copy()
    # df_copy = df_copy[df_copy["country name"] == option_slctd]

    print(df_copy)

    # Plotly Express
    fig = px.bar(df_copy, x=option_slctd, y='country name', orientation='h')
    fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending', 'tickmode': 'linear', 'tickfont': {'size': 9}}, margin_b=10, margin_t=10, margin_l=10, margin_r=10)
 
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)