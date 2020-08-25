#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import os
import sys
import pandas as pd


new_names = {
    'date': 'date',
    'name': 'name',
    'category': 'cat',
    'amount': 'amount',
    'notes_and_#tags': 'note',
    'description': 'desc',
    'category_split': 'split',
    'transaction_id': 'id'
}


def load_data():
    url = 'https://docs.google.com/spreadsheets/d/'
    sheet_id = '1N9obnCF3fdjq2sOL0uvkVhbhpmZFOtkssXjCdTGfJak'
    tab_id = '1646235209'
    path = f'{url}{sheet_id}/export?format=csv&gid={tab_id}'
    return pd.read_csv(path,
                       parse_dates={'date': ['Date', 'Time']},
                       dayfirst=True)


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


def select_cols(df):
    return df[new_names]


def rename_cols(df):
    df = df.rename(columns=new_names)
    return df


def add_variables(df):
    df['ym'] = df.date.dt.to_period('M').dt.to_timestamp()
    return df


def order_cols(df):
    first = ['date', 'desc', 'cat', 'amount', 'name', 'note']
    rest = sorted(list(set(df.columns) - set(first)))
    return df[first + rest]


def save_data(df):
    ROOTDIR = os.getcwd()
    PATH = os.path.join(ROOTDIR, 'data', 'clean.parquet')
    df.to_parquet(PATH, compression='BROTLI')


def main(argv=None):
    return (
        load_data()
        .pipe(clean_names)
        .pipe(clean_str)
        .pipe(select_cols)
        .pipe(rename_cols)
        .pipe(add_variables)
        .pipe(order_cols)
        .pipe(save_data)
    )


if __name__ == '__main__':
    sys.exit(main())
