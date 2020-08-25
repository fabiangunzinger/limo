#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# visit http://127.0.0.1:8050/ in your web browser.
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


ROOT = os.getcwd()
PATH = os.path.join(ROOT, 'data', 'clean.parquet')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def drop_transfers(df):
    transfers = (
        (df.cat.eq('transfer')) |
        (df.merch.str.contains(' pot', na=False))
    )
    return df[~transfers]


def income_spending(df):
    fig = make_subplots()

    fig.add_trace(
        go.Bar(
            x=df[df.amount > 0].ym,
            y=df[df.amount > 0].amount,
        )
    )
    fig.add_trace(
        go.Bar(
            x=df[df.amount < 0].ym,
            y=df[df.amount < 0].amount,
            marker_color='indianred'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.groupby('ym').ym.first(),
            y=df.groupby('ym').amount.sum(),
            mode='markers',
            marker=dict(
                color='green',
                line_width=2,
                line_color='white',
                size=10
            )
        )
    )
    fig.update_layout(
        barmode='relative',
        xaxis_title='Month',
        yaxis_title='Spending / Income',
        showlegend=False
    )
    fig.show()


df = pd.read_parquet(PATH)

preproc = drop_transfers(df)
fig = income_spending(preproc)


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
