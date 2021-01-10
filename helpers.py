import os
import pandas as pd

def read_monzo():
    """Read data from Monzo google sheet."""
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


def read_budget():
    url = os.environ.get('BUDGET_URL')
    sheet_id = os.environ.get('BUDGET_SHEETID')
    tab_id = os.environ.get('BUDGET_TABID')
    path = f'{url}{sheet_id}/export?format=csv&gid={tab_id}'
    df = pd.read_csv(path, usecols=[0, 1], names=['category', 'budget'],
                     skiprows=27, skipfooter=35, engine='python',
                     converters={'category': str.lower})
    return df

