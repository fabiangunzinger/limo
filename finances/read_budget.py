#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import pandas as pd


def fetch_raw():
    url = os.environ.get('BUDGET_URL')
    sheet_id = os.environ.get('BUDGET_SHEETID')
    tab_id = os.environ.get('BUDGET_TABID')
    path = f'{url}{sheet_id}/export?format=csv&gid={tab_id}'
    return pd.read_csv(path)


def clean_names(df):
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(' ', '_')
    )
    return df


def clean_str(df):
    strs = df.select_dtypes('object')
    strs = strs.apply(lambda col: col.str.lower())
    df[strs.columns] = strs
    return df


def get_spending_breakdown(df):
    return df.iloc[20:35]


def clean_frame(df):
    df = df[['item', 'monthly']]
    df.columns = ['cat', 'budget']
    return df


def read_budget():
    return (
        fetch_raw()
        .pipe(clean_names)
        .pipe(clean_str)
        .pipe(get_spending_breakdown)
        .pipe(clean_frame)
    )


def main(argv=None):
    return read_budget()


if __name__ == '__main__':
    sys.exit(main())
