#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# colors here: https://htmlcolorcodes.com

# visit http://127.0.0.1:8050/ in your web browser.
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from finances.cat_spend import make_cat_spend_fig
from finances.budget_check import make_budget_check_fig


colors = {
    'backgroundMain': '#FFFFFF',
    'backgroundFinances': '#FFFFFF',
    'backgroundExper': '#FFFFFF',
    'text': '#000000'
}
fig_config = {
    'scrollZoom': False,
    'displayModeBar': True
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={
        'backgroundColor': colors['backgroundMain'],
        'color': colors['text']
    },
    children=[
        html.H1(
            "Life Monitor",
            style={
                'textAlign': 'center',
            }),

        html.Div(
            style={'backgroundColor': colors['backgroundFinances']},
            children=[
                html.H3('Finances'),

                dcc.Graph(
                    figure=make_cat_spend_fig(),
                    config=fig_config
                ),

                dcc.Dropdown(
                    id='selector',
                    options=[
                        {'label': 'Aug 2020', 'value': '2020-08'},
                        {'label': 'July 2020', 'value': '2020-07'},
                    ],
                    multi=False,
                    value='2020-08',
                    style={'width': '40%'},
                ),

                html.Div(id='announcer', children=[]),

                dcc.Graph(
                    id='budget_checker',
                    figure={},
                    config=fig_config
                ),
            ]
        ),
    ]
)


@ app.callback(
    [Output(component_id='announcer', component_property='children'),
     Output(component_id='budget_checker', component_property='figure')],
    [Input(component_id='selector', component_property='value')]
)
def updater(ym):
    fig = make_budget_check_fig(ym)
    announcement = f'Period selected is: {ym}'
    return announcement, fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
