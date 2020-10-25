import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    return html.H5("Life monitor")


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/life-monitor/overview",
                className="tab first",
            ),
            dcc.Link(
                "Finances",
                href="/life-monitor/finances",
                className="tab",
            ),
            dcc.Link(
                "Health",
                href="/life-monitor/health",
                className="tab",
            ),
        ],
        className="all-tabs",
    )
    return menu
