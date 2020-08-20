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
    'description': 'desc'
}


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    return parser.parse_args()


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


def order_cols(df):
    return df[['date', 'desc', 'cat', 'amount', 'name', 'note']]


def save_data(df):
    ROOTDIR = os.getcwd()
    PATH = os.path.join(ROOTDIR, 'data', 'clean', 'clean.csv')
    df.to_csv(PATH)


def read_data(path):
    (pd.read_csv(path, parse_dates={'date': [1, 2]})
     .pipe(clean_names)
     .pipe(clean_str)
     .pipe(select_cols)
     .pipe(rename_cols)
     .pipe(order_cols)
     .pipe(save_data))


def main(argv=None):
    if argv is None:
        argv = sys.argv[:1]
    args = parse_args(argv)
    read_data(args.path)


if __name__ == '__main__':
    sys.exit(main())
