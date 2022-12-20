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

country_stats = {
    'country name' : [], 
    'country ranking': [], 
    'average possession': [],
    'total goals': [], 
    'total passes': [], 
    'total shots': [], 
    'total shots on target': [],
    'country avg goals': [],
    'country avg passes': [],
    'country avg shots on target': [],
    'country avg yellow cards': [],
    'country avg red cards': [],
    'country avg free kicks': [],
    'country avg corners': [],
    'country avg fouls': []
    }

average_stats = {
    'total avg possession': 0, 
    'total avg goals': 0, 
    'total avg passes': 0, 
    'total avg shots on target': 0, 
    'total avg yellow cards': 0, 
    'total avg red cards': 0, 
    'total avg free kicks': 0,
    'total avg corners': 0,
    'total avg fouls': 0
    }

for i in csv_extra_dataframe.index:
    avg_possession = 0
    total_goals = 0
    total_passes = 0
    total_shots = 0
    total_shots_on_target = 0
    total_free_kicks = 0
    total_corners = 0
    total_fouls = 0
    total_yellows = 0
    total_reds = 0
    game_count = 0
    team_name = csv_extra_dataframe['Country'][i]
    country_stats['country ranking'].append(32-i)

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
            total_free_kicks += csv_main_dataframe['free kicks team1'][j]
            total_corners += csv_main_dataframe['corners team1'][j]
            total_fouls += csv_main_dataframe['fouls against team2'][j]
            total_yellows += csv_main_dataframe['yellow cards team1'][j]
            total_reds += csv_main_dataframe['red cards team1'][j]

        if second_team_name == team_name:
            game_count += 1
            avg_possession += csv_main_dataframe['possession team2'][j]
            total_goals += csv_main_dataframe['number of goals team2'][j]
            total_passes += csv_main_dataframe['passes completed team2'][j]
            total_shots += csv_main_dataframe['total attempts team2'][j]
            total_shots_on_target += csv_main_dataframe['on target attempts team2'][j]
            total_free_kicks += csv_main_dataframe['free kicks team2'][j]
            total_corners += csv_main_dataframe['corners team2'][j]
            total_fouls += csv_main_dataframe['fouls against team1'][j]
            total_yellows += csv_main_dataframe['yellow cards team2'][j]
            total_reds += csv_main_dataframe['red cards team2'][j]

    total_avg_possession = (avg_possession*100)/game_count
    country_stats['country name'].append(team_name)
    country_stats['average possession'].append(total_avg_possession)
    country_stats['total goals'].append(total_goals)
    country_stats['total passes'].append(total_passes)
    country_stats['total shots'].append(total_shots)
    country_stats['total shots on target'].append(total_shots_on_target)
    country_stats['country avg goals'].append(total_goals/game_count)
    country_stats['country avg passes'].append(total_passes/game_count)
    country_stats['country avg shots on target'].append(total_shots_on_target/game_count)
    country_stats['country avg yellow cards'].append(total_yellows/game_count)
    country_stats['country avg red cards'].append(total_reds/game_count)
    country_stats['country avg free kicks'].append(total_free_kicks/game_count)
    country_stats['country avg corners'].append(total_corners/game_count)
    country_stats['country avg fouls'].append(total_fouls/game_count)

    average_stats['total avg possession'] += total_avg_possession
    average_stats['total avg goals'] += total_goals/game_count
    average_stats['total avg passes'] += total_passes/game_count
    average_stats['total avg shots on target'] += total_shots_on_target/game_count
    average_stats['total avg yellow cards'] += total_yellows/game_count
    average_stats['total avg red cards'] += total_reds/game_count
    average_stats['total avg free kicks'] += total_free_kicks/game_count
    average_stats['total avg corners'] += total_corners/game_count
    average_stats['total avg fouls'] += total_fouls/game_count

average_stats['total avg possession'] = average_stats['total avg possession']/32
average_stats['total avg goals'] = average_stats['total avg goals']/32
average_stats['total avg passes'] = average_stats['total avg passes']/32
average_stats['total avg shots on target'] = average_stats['total avg shots on target']/32
average_stats['total avg yellow cards'] = average_stats['total avg yellow cards']/32
average_stats['total avg red cards'] = average_stats['total avg red cards']/32
average_stats['total avg free kicks'] = average_stats['total avg free kicks']/32
average_stats['total avg corners'] = average_stats['total avg corners']/32
average_stats['total avg fouls'] = average_stats['total avg fouls']/32

country_stats_dataframe = pd.DataFrame(country_stats)

image_path = 'assets/istockphoto-1176781177-612x612.jpg'

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
        style={'width': "40%", 'height': '100%', 'margin-left': '4%'},
        ),

    html.Div([
        dcc.Graph(
            id='team_rankings', 
            figure={}, 
            style={'maxHeight': '400px', 'display': 'inline-block', 'overflowY': 'scroll'}, 
            config={'displayModeBar': False},
        ),
        html.Img(
            src=image_path, 
            style={'display': 'inline-block', 'margin-right': '20px', 'margin-left': '4%'}
        )
    ], style={'display': 'flex'}),

    html.Div([
        dcc.Dropdown(id='slct_country', options=[{'label': 'Argentina', 'value': 'ARGENTINA'},
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
        {'label': 'Qatar', 'value': 'QATAR'}],
        multi=False,
        value='ARGENTINA',
        style={'width': "40%", 'height': '100%', 'margin-left': '4%'},
        ),

        dcc.Graph(
            id='team_vs_average', 
            figure={}, 
            style={'maxHeight': '40', 'display': 'inline-block', 'overflowY': 'scroll'}, 
            config={'displayModeBar': False},
        )]),
])

# ------------------------------------------------------------------------------------------
# Connect Plotly Graph to Dash components
@app.callback(
    Output(component_id='team_rankings', component_property='figure'),
    Input(component_id='slct_stat', component_property='value')
)
def update_ranking_graph(option_slctd):
    df_copy = country_stats_dataframe.copy()
    fig = px.bar(df_copy, x=option_slctd, y='country name', orientation='h')
    fig.update_layout(
        barmode='stack', 
        plot_bgcolor='#fff',
        height=700, 
        yaxis={'categoryorder': 'total ascending', 'tickmode': 'linear', 'tickfont': {'size': 15}}, 
        margin_b=10, 
        margin_t=10, 
        margin_l=10, 
        margin_r=10
    )
    return fig

@app.callback(
    Output(component_id='team_vs_average', component_property='figure'),
    Input(component_id='slct_country', component_property='value')
)
def update_team_average_graph(option):
    df_country_copy = country_stats_dataframe.copy()
    df_country_copy = df_country_copy.loc[df_country_copy['country name'] == option]
    comparison_dictionary = {
        'stat name': 
            ['average possession', 
            'average goals', 
            'average shots on target', 
            'average free kicks', 
            'average corners', 
            'average fouls', 
            'average yellow cards', 
            'average red cards'],
        'average values': 
            [average_stats['total avg possession'], 
            average_stats['total avg goals'], 
            average_stats['total avg shots on target'], 
            average_stats['total avg free kicks'], 
            average_stats['total avg corners'],
            average_stats['total avg fouls'],
            average_stats['total avg yellow cards'],
            average_stats['total avg red cards']],
        'team_values': 
            [df_country_copy.loc[0].at['average possession'],
            df_country_copy.loc[0].at['country avg goals'],
            df_country_copy.loc[0].at['country avg shots on target'],
            df_country_copy.loc[0].at['country avg free kicks'],
            df_country_copy.loc[0].at['country avg corners'],
            df_country_copy.loc[0].at['country avg fouls'],
            df_country_copy.loc[0].at['country avg yellow cards'],
            df_country_copy.loc[0].at['country avg red cards']]
        }

    stat_names = comparison_dictionary['stat name']
    average_values = comparison_dictionary['average values']
    team_values = comparison_dictionary['team_values']

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=stat_names,
        y=average_values,
        name='Average values'
    ))
    fig1.add_trace(go.Bar(
        x=stat_names,
        y=team_values,
        name='Team values'
    ))
    fig1.update_layout(title='Grouped bar chart', xaxis_title='Stat name', yaxis_title='Value', autosize=False,
    width=500,
    height=500)
    fig1.show()


if __name__ == '__main__':
    app.run_server(debug=True)