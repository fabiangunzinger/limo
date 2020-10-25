#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import pandas as pd


def fetch_raw():
    url = os.environ.get('MONZO_URL')
    sheet_id = os.environ.get('MONZO_SHEETID')
    tab_id = os.environ.get('MONZO_TABID')
    path = f'{url}{sheet_id}/export?format=csv&gid={tab_id}'
    return pd.read_csv(path, dayfirst=True,
                       parse_dates={'date': ['Date', 'Time']})


def clean_names(df):
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(' ', '_')
    )
    return df


def clean_str(df):
    strs = df.select_dtypes('object')
    strs = strs.apply(lambda x: x.str.lower())
    df[strs.columns] = strs
    return df


def select_rename_cols(df):
    new_names = {
        'date': 'date',
        'name': 'merch',
        'category': 'cat',
        'amount': 'amount',
        'notes_and_#tags': 'note',
        'description': 'desc',
        'category_split': 'split',
        'transaction_id': 'id',
        'type': 'type',
    }
    df = df[new_names]
    return df.rename(columns=new_names)


def add_month(df):
    df['month'] = df.date.dt.to_period('M').dt.to_timestamp()
    return df


def categorise_transfers(df):
    mask = (
        (df.cat.eq('transfer')) |
        (df.type.eq('pot transfer')) |
        (df.note.eq('fgtofg'))
    )
    df.loc[mask, 'cat'] = 'transfer'
    return df


def invert_amounts(df):
    df['amount'] = df.amount * -1
    return df


def order_cols(df):
    first = ['date', 'desc', 'cat', 'amount', 'merch', 'note']
    rest = sorted(list(set(df.columns) - set(first)))
    return df[first + rest]


def read_monzo():
    return (
        fetch_raw()
        .pipe(clean_names)
        .pipe(clean_str)
        .pipe(select_rename_cols)
        .pipe(add_month)
        .pipe(categorise_transfers)
        .pipe(invert_amounts)
        .pipe(order_cols)
    )


def main(argv=None):
    return read_monzo()


if __name__ == '__main__':
    sys.exit(main())