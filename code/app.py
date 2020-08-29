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

colors = {
    'backgroundMain': '#111111',
    'backgroundFinances': 'green',
    'text': '#7FDBFF'
}


def drop_transfers(df):
    transfers = (
        (df.cat.eq('transfer')) |
        (df.merch.str.contains(' pot', na=False))
    )
    return df[~transfers]


def make_credit_data(df):
    last5mnths = df.ym.drop_duplicates().nlargest(5)
    data = df[df.amount < 0].copy()
    data = data[data.ym.isin(last5mnths)]
    data['amount'] = data.amount * -1
    return data


def income_spending(df):
    g = df.groupby('ym')
    fig = (
        px.bar(
            x=df.ym,
            y=df.amount,
            color=df.amount > 0
        )
        .add_scatter(
            x=g.ym.first(),
            y=g.amount.sum(),
            mode='markers',
            marker=dict(
                color='green',
                line_width=2,
                line_color='white',
                size=10
            )
        )
        .update_layout(
            barmode='relative',
            xaxis_title='Month',
            yaxis_title='Spending / Income',
            xaxis_type='category',
            showlegend=False,
            plot_bgcolor=colors['backgroundFinances'],
            paper_bgcolor=colors['backgroundFinances'],
            font_color=colors['text']
        )
    )
    return fig


def group_spending(df):
    g = df.groupby(['ym', 'cat'])
    fig = (
        px.bar(
            x=g.ym.first(),
            y=g.amount.sum(),
            color=g.cat.first()
        )
        .update_layout(
            xaxis_title='Month',
            yaxis_title='Spending',
            xaxis_type='category',
            legend_title_text='Category',
            plot_bgcolor=colors['backgroundFinances'],
            paper_bgcolor=colors['backgroundFinances'],
            font_color=colors['text']
        )
        .add_shape(
            type='line',
            yref='y',
            xref='paper',
            x0=0,
            y0=1750,
            x1=1,
            y1=1750,
            line=dict(
                color="blue",
                width=4,
                dash="dashdot",
            )
        )
    )
    return fig


intro_text = """
The idea of this is to have one place to view all things that matter to me in life.
"""

df = pd.read_parquet(PATH)
preproc = drop_transfers(df)
credits = make_credit_data(preproc)


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

        dcc.Markdown(intro_text),

        html.Div(
            style={'backgroundColor': colors['backgroundFinances']},
            children=[
                html.H3('Finances'),

                dcc.Graph(
                    figure=income_spending(preproc),
                ),

                dcc.Graph(
                    figure=group_spending(credits),
                ),
            ]
        ),

        html.Div(
            'Hello world. Some more text here.'
        )

    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='127.0.0.1')
    # print(os.getcwd())
