#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# visit http://127.0.0.1:8050/ in your web browser.
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

ROOT = os.getcwd()
PATH = os.path.join(ROOT, 'data', 'clean.parquet')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def in_out(df):
    fig = px.bar(df, x='ym', y='amount',
                 color=df.amount > 0)
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Spent',
        showlegend=False
    )
    return fig


df = pd.read_parquet(PATH)
fig = in_out(df)


app.layout = html.Div(
    children=[

        html.H1(
            children="Finance dashboard",
            style={
                'textAlign': 'center',
            }),

        html.Div(
            children='A simple dashboard to keep track of my spending.',
            style={
                'textAlign': 'center',
            }),
        #
        dcc.Graph(
            id='example-graph',
            figure=fig
        ),

    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
    # print(os.getcwd())
