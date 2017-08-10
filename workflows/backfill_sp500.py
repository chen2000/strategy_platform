from __future__ import absolute_import

from collections import namedtuple
import csv
from math import isnan
import os
import pandas as pd

from config.config import settings
from strategy_platform.preprocess.yahoo_download import download_batch
from strategy_platform.preprocess.make_file import make_input_file, make_output_file
from strategy_platform.technical.indicators import ma, b_bands, macd, rsi, sto_k, sto_d
from strategy_platform.technical.plots import create_ta_charts
from strategy_platform.strategies.test_triggers import trigger_symbol_stats, trigger_index_stats
from strategy_platform.utils import strdate_add, strdate_subtract


start_date = '2007-01-01'
end_date = '2017-05-11'
index = 'sp500'
force_rerun = True
force_rerun_ta = True

# load symbol name
with open(make_input_file(index)) as csvfile:
    symbols = [row[0] for ind, row in enumerate(csv.reader(csvfile.read().splitlines())) if ind > 0]

# download Yahoo finance trading data for all symbols in the index
if force_rerun:
   # download trading data
    download_batch(
                    symbols, 
                    index, 
                    start_date, 
                    end_date, 
                    'd', 
                    make_output_file(index, 'daily'))
    download_batch(
                    symbols, 
                    index, 
                    start_date, 
                    end_date, 
                    'w', 
                    make_output_file(index, 'weekly'))
daily_data = pd.read_csv(make_output_file(index, 'daily'))
weekly_data = pd.read_csv(make_output_file(index, 'weekly'))

if force_rerun_ta:
    # calculate TA indicators for each symbol
    symbols = daily_data.Symbol.unique()
    directory = os.path.join(settings['folder']['trading'], index)
    if not os.path.exists(directory):
        os.mkdir(directory)
    for symbol in symbols:
        fname = os.path.join(directory, symbol + '_ta.csv')
        if force_rerun == False and os.path.exists(fname):
            continue
        df = daily_data.loc[daily_data['Symbol'] == symbol]
        df = df.iloc[::-1].reset_index().drop('index', axis=1)
        df = ma(df, 20)
        df = ma(df, 50)
        df = b_bands(df, 20)
        df = rsi(df, 14)
        df = sto_k(df, 14)
        df = sto_d(df, 14)
        df = macd(df, 12, 26)
        df.to_csv(fname, index=False)

        wfname = os.path.join(directory, symbol + '_weekly_ta.csv')
        wdf = weekly_data.loc[weekly_data['Symbol'] == symbol]
        wdf = wdf.iloc[::-1].reset_index().drop('index', axis=1)
        wdf = ma(wdf, 20)
        wdf = ma(wdf, 50)
        wdf = rsi(wdf, 14)
        wdf.to_csv(wfname, index=False)
# ============= end downloading and preprocessing data ==================


# plot per symbol
# pick up any symbol and time period, create charts, note: ~ 252 trading days per year for NYSE
# for symbol in symbols:
#     create_ta_charts(symbol, index, start_date, end_date, strdate_subtract(end_date, 365), end_date)

# set parameters
a, b, success_window = 5, 2, 3
# test rules per symbol
# e.g. GS, macd corss up, 5 consecutive neg values followed by 2 positive values
accumulated_trigger_table = []
for symbol in symbols:
    (stats_table, trigger_table) = trigger_symbol_stats(symbol, index, a, b, success_window)
    accumulated_trigger_table += trigger_table
with open('data/results/accumulated_trigger_table_sp500.csv', 'wt') as csvfile:
    csv.writer(csvfile, delimiter=",").writerows(accumulated_trigger_table)


