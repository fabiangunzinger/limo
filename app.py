#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# colors here: https://htmlcolorcodes.com

# multi-page framework here: https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-financial-report/app.py

# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import (
    finances,
    health
)

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# register all callbacks - find nicer solution
# discussion here: https://community.plotly.com/t/dash-callback-in-
# a-separate-file/14122/12
finances.register_callbacks(app)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/life-monitor/overview":
        return finances.create_layout(app)
    elif pathname == "/life-monitor/finances":
        return finances.create_layout(app)
    elif pathname == "/life-monitor/health":
        return health.create_layout(app)
    else:
        return finances.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True)
