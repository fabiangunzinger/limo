import os
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from pages.header import Header


def create_layout(app):
    return html.Div(
        [
            Header(app),
            html.H3(
                "Health", style={'textAlign': 'center'}
            ),
            html.H6('No data yet'),
        ]
    )
