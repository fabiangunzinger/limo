#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import pandas as pd


def read_budget():
    url = os.environ.get('BUDGET_URL')
    sheet_id = os.environ.get('BUDGET_SHEETID')
    tab_id = os.environ.get('BUDGET_TABID')
    path = f'{url}{sheet_id}/export?format=csv&gid={tab_id}'
    # df = pd.read_csv(path)
    print(url)
    return url


read_budget()

#     df.columns = df.columns.str.lower().str.replace(' ', '_')
#
#     strs = df.select_dtypes('object')
#     df[strs.columns] = strs.apply(lambda col: col.str.lower())
#
#
#
# def clean_frame(df):
#     df = df[['item', 'monthly']]
#     df.columns = ['cat', 'budget']
#     return df
#
#
# def read_budget():
#     return (
#         fetch_raw()
#         .pipe(clean_names)
#         .pipe(clean_str)
#         .pipe(get_spending_breakdown)
#         .pipe(clean_frame)
#     )
#
