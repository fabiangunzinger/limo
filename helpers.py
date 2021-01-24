import os
import numpy as np
import pandas as pd

def read_monzo(raw=False):
    """Read data from Monzo google sheet."""
    url = os.environ.get('MONZO_URL')
    sheet_id = os.environ.get('MONZO_SHEETID')
    tab_id = os.environ.get('MONZO_TABID')
    fp = f'{url}{sheet_id}/export?format=csv&gid={tab_id}'
    df = pd.read_csv(fp, dayfirst=True, parse_dates=['Date'])
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('#', '')
    )
    # lowercase strings and string NA values for easy re search
    str_cols = df.select_dtypes('object')
    df[str_cols.columns] = str_cols.apply(lambda x: x.str.lower())
    df = df.fillna('missing')
    # short names for lazy typers
    df = df.rename(columns={
        'notes_and_tags': 'notes',
        'category': 'cat',
        'description': 'desc',
    })
    return df
    

def clean_monzo(df):
    df = df.copy()
    useful_cols = ['date', 'desc', 'amount', 'cat', 'name', 'notes', 'type']
    df = df[useful_cols]
    
    # invert amount so spend is positive
    df['amount'] = df.amount.mul(-1)

    # classify pot ans 'hsbc help to buy' transfers as savings
    savings = (df.type == 'pot transfer') | (df.desc == 'help to buy')
    df['cat'] = np.where(savings, 'savings', df.cat)
    
    # make income count for next month 
    offset = pd.offsets.MonthBegin(1)
    df['date'] = np.where(df.cat == 'income', df.date + offset, df.date) 

    # groups
    df['group'] = np.where(df.cat == 'income', 'income', None)
    df['group'] = np.where(df.cat == 'savings', 'savings', df.group)
    df['group'] = np.where(df.group.isna(), 'spending', df.group)
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

