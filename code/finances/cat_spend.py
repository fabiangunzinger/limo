import plotly.express as px

from finances.read_monzo import read_monzo


def cat_spend_data():
    monzo = read_monzo()
    return (
        monzo
        .pivot_table('amount', 'month', 'cat', aggfunc='sum', fill_value=0)
        .reset_index()
        .melt(id_vars=['month'], value_name='amount')
    )


def cat_spend_figure(df):
    g = df.groupby('month')
    fig = (
        px.bar(
            df,
            x='month',
            y='amount',
            color='cat',
            template='simple_white',
            hover_name='cat',
            # hover_data=['month', 'amount']
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


def make_cat_spend_fig():
    data = cat_spend_data()
    return cat_spend_figure(data)
