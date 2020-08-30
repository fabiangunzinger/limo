#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# colors here: https://htmlcolorcodes.com

# visit http://127.0.0.1:8050/ in your web browser.
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


ROOT = os.getcwd()
PATH = os.path.join(ROOT, 'data', 'clean.parquet')

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


def group_spending(df):
    g = df.groupby('ym')
    fig = (
        px.bar(
            df,
            x='ym',
            y='amount',
            color='cat',
            template='simple_white',
            hover_name='cat',
            # hover_data=['ym', 'amount']
        )
        .add_scatter(
            x=g.ym.first(),
            y=g.amount.mean(),
            showlegend=False,
            mode='markers',
            marker=dict(
                color='#EF9A9A',
                line_width=2,
                line_color='white',
                size=10
            )
        )
        .update_xaxes(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        .update_layout(
            xaxis_title='Month',
            yaxis_title='Income / Spending',
            # xaxis_type='category',
            xaxis_tickformat='%b %Y',
            xaxis_tickangle=30,
            showlegend=False,
            # plot_bgcolor=colors['backgroundFinances'],
            # paper_bgcolor=colors['backgroundFinances'],
            # font_color=colors['text']
        )
    )
    return fig


intro_text = """
The idea of this is to have one place to view all things that matter to me in life.
"""


# Finance

df = pd.read_parquet(PATH)
agg = (df
       .pivot_table('amount', 'ym', 'cat', aggfunc='sum', fill_value=0)
       .reset_index()
       .melt(id_vars=['ym'], value_name='amount'))

fin1 = group_spending(agg)


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
                    figure=fin1,
                    config=fig_config
                ),
            ]
        ),


        # html.Div(
        #     style={'backgroundColor': colors['backgroundExper']},
        #     children=[
        #         html.H3('Finance'),
        #
        #         dcc.Dropdown(
        #             id='selector',
        #             options=[
        #                 {'label': 'all', 'value': 2019},
        #                 {'label': '2020', 'value': 2020},
        #             ],
        #             multi=False,
        #             value=2019,
        #             style={'width': '40%'},
        #         ),
        #
        #         html.Div(id='announcer', children=[]),
        #
        #         dcc.Graph(id='monthly_spend', figure={})
        #     ]
        # )

    ])


# @app.callback(
#     [Output(component_id='announcer', component_property='children'),
#      Output(component_id='monthly_spend', component_property='figure')],
#     [Input(component_id='selector', component_property='value')]
# )
# def graph_updater(year):
#
#     print(f'Year selected: {year}')
#
#     announcement = f'Year selected is: {year}'
#
#     dd = df.copy()
#     dd = dd[dd.date.dt.year.eq(year)]
#     dd = drop_transfers(dd)
#     dd = make_credit_data(dd)
#     fig = group_spending(dd)
#
#     return announcement, fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
    # print(os.getcwd())
