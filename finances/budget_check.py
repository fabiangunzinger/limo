import plotly.express as px

from finances.read_monzo import read_monzo
from finances.read_budget import read_budget


def make_data(month='2020-08'):
    monzo = (
        read_monzo()
        .loc[lambda df: df.month.eq(month)]
        .rename(columns={'amount': 'actual'})
        .pivot_table(values='actual', index='cat', aggfunc='sum')
        .reset_index()
    )
    budget = read_budget()
    merged = (
        monzo
        .merge(budget)
        .melt(id_vars=['cat'], var_name='var', value_name='amount')
        .sort_values(['var', 'amount'], ascending=True)
    )
    return merged


def make_figure(df):
    fig = (
        px.scatter(
            df,
            x='amount',
            y='cat',
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


def make_budget_check_fig(month):
    return make_figure(make_data(month))
