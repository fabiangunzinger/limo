import os
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from pages.header import Header

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


def create_layout(app):
    return html.Div(
        className="container",
        children=[
            Header(app),
            html.H3(
                "Finances", style={'textAlign': 'center'}
            ),
            html.Div(
                [
                    html.H6('Overview'),
                    dcc.Graph(
                        figure=monthly_overview(),
                        config=fig_config
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id='selector',
                        options=[
                            {'label': 'Oct 2020', 'value': '2020-10'},
                            {'label': 'Sep 2020', 'value': '2020-09'},
                            {'label': 'Aug 2020', 'value': '2020-08'},
                            {'label': 'July 2020', 'value': '2020-07'},
                        ],
                        multi=False,
                        value='2020-10',
                        style={'width': '40%'},
                    ),
                    html.Div(
                        id='informer'
                    ),
                    dcc.Graph(
                        id='budget_checker',
                        figure={},
                        config=fig_config
                    ),
                ]
            ),
        ],
    )


def register_callbacks(app):
    @ app.callback(
        [Output(component_id='informer', component_property='children'),
         Output(component_id='budget_checker', component_property='figure')],
        [Input(component_id='selector', component_property='value')]
    )
    def updater(month):
        fig = budget_check(month)
        info = f'Period selected is: {month}'
        return info, fig


def read_budget():
    url = os.environ.get('BUDGET_URL')
    sheet_id = os.environ.get('BUDGET_SHEETID')
    tab_id = os.environ.get('BUDGET_TABID')
    path = f'{url}{sheet_id}/export?format=csv&gid={tab_id}'
    df = pd.read_csv(path, usecols=[0, 1], names=['category', 'budget'],
                     skiprows=27, skipfooter=35, engine='python',
                     converters={'category': str.lower})
    return df


def read_monzo():
    url = os.environ.get('MONZO_URL')
    sheet_id = os.environ.get('MONZO_SHEETID')
    tab_id = os.environ.get('MONZO_TABID')
    path = f'{url}{sheet_id}/export?format=csv&gid={tab_id}'
    df = (pd.read_csv(path, dayfirst=True,
                      parse_dates={'date': ['Date', 'Time']}))

    df.columns = (df.columns.str.lower()
                  .str.replace(' ', '_')
                  .str.replace('#', ''))

    strs = df.select_dtypes('object')
    df[strs.columns] = strs.apply(lambda x: x.str.lower())
    df['amount'] = df.amount.mul(-1)

    # monthly variable with new month starting on 25th
    shift = pd.TimedeltaIndex(df.date.dt.daysinmonth - 25 + 1, unit='D')
    shifted = df.date + shift
    df['month'] = shifted.dt.to_period('M').dt.to_timestamp()

    # categorise transfers
    mask = (
        (df.category.eq('transfer')) |
        (df.type.eq('pot transfer')) |
        (df.notes_and_tags.eq('fgtofg'))
    )
    df.loc[mask, 'category'] = 'transfer'

    return df


monzo = read_monzo()
budget = read_budget()


def monthly_overview():
    """Overview of monthly spend by category for the last n months."""
    df = (
        read_monzo()
        .pivot_table('amount', 'month', 'category',
                     aggfunc='sum', fill_value=0)
        .reset_index()
        .melt(id_vars=['month'], value_name='amount')
    )
    g = df.groupby('month')
    fig = (
        px.bar(
            df,
            x='month',
            y='amount',
            color='category',
            template='simple_white',
            hover_name='category',
        )
        .add_scatter(
            x=g.month.first(),
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
                buttons=list(
                    [
                        dict(
                            count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"
                        ),
                        dict(
                            count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"
                        ),
                        dict(
                            count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"
                        ),
                        dict(
                            step="all"
                        ),
                    ]
                )
            )
        )
        .update_layout(
            xaxis_title='Month',
            yaxis_title='Income / Spending',
            xaxis_tickformat='%b %Y',
            xaxis_tickangle=30,
            showlegend=False,
        )
    )
    return fig


def budget_check(month='2020-08'):
    monzo_pivot = (
        read_monzo()
        .loc[lambda df: df.month.eq(month)]
        .rename(columns={'amount': 'actual'})
        .pivot_table(values='actual', index='category', aggfunc='sum')
        .reset_index()
    )
    df = (
        monzo_pivot
        .merge(read_budget(), how='right')
        .fillna(0)
        .melt(id_vars=['category'], var_name='var', value_name='amount')
        .sort_values(['var', 'amount'], ascending=True)
    )
    fig = (
        px.scatter(
            df,
            x='amount',
            y='category',
            color='var',
            color_discrete_sequence=[
                'rgba(156, 165, 196, 0.95)',
                'rgba(204, 204, 204, 0.95)',
            ]
        )
        .update_layout(
            xaxis_title='Amount (£)',
            yaxis_title=None,
            xaxis=dict(
                showgrid=False,
                showline=True,
                linecolor='rgb(102, 102, 102)',
                tickfont_color='rgb(102, 102, 102)',
                showticklabels=True,
                dtick=100,
                ticks='outside',
                tickcolor='rgb(102, 102, 102)',
            ),
            legend=dict(
                title=None,
                orientation='h',
                font_size=10,
                yanchor='bottom',
                y=0,
                xanchor='right',
                x=1,
            ),
            width=800,
            height=600,
            hovermode='closest',
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        .update_traces(
            mode='markers',
            marker=dict(
                line_width=1,
                symbol='circle',
                size=16,
                line_color='rgba(217, 217, 217, 1.0)'
            )
        )
    )
    return fig
