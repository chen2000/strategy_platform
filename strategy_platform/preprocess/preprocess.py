from __future__ import absolute_import

from collections import namedtuple
import csv
from math import isnan
import os
import pandas as pd

from config.config import settings
from strategy_platform.preprocess.data_download import download_batch
from strategy_platform.preprocess.make_file import make_input_file, make_output_file
from strategy_platform.technical.indicators import ma, b_bands, macd, rsi, sto_k, sto_d
#from strategy_platform.technical.plots import create_ta_charts
from strategy_platform.strategies.test_triggers import trigger_symbol_stats, trigger_index_stats
from strategy_platform.utils import strdate_add, strdate_subtract


def preprocess(source, index, start_date, end_date, force_rerun=True, force_rerun_ta=True):
    # load symbol name
    with open(make_input_file(index)) as csvfile:
        symbols = [row[0] for ind, row in enumerate(csv.reader(csvfile.read().splitlines())) if ind > 0]

    # download Yahoo finance trading data for all symbols in the index
    if force_rerun:
       # download trading data
        download_batch(
            source,
            symbols, 
            index, 
            start_date, 
            end_date, 
            'd', 
            make_output_file(index, 'daily'))
        daily_data = pd.read_csv(make_output_file(index, 'daily'))

        if source == 'yahoo':    # only yahoo provide weekly data
            download_batch(
                source,
                symbols, 
                index, 
                start_date, 
                end_date, 
                'w', 
                make_output_file(index, 'weekly'))
            weekly_data = pd.read_csv(make_output_file(index, 'weekly'))    

    if force_rerun_ta:
        # calculate TA indicators for each symbol
        symbols = daily_data.Symbol.unique()
        directory = os.path.join(settings['folder']['trading'], index)
        if not os.path.exists(directory):
            os.mkdir(directory)
        for symbol in symbols:
            fname = os.path.join(directory, symbol + '_ta.csv')

            if source in ('g_1year', 'quandl'):  # avoid overwrite
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

            if source == 'yahoo':    #only yahoo provides weekly data
                wfname = os.path.join(directory, symbol + '_weekly_ta.csv')
                wdf = weekly_data.loc[weekly_data['Symbol'] == symbol]
                wdf = wdf.iloc[::-1].reset_index().drop('index', axis=1)
                wdf = ma(wdf, 20)
                wdf = ma(wdf, 50)
                wdf = rsi(wdf, 14)
                wdf.to_csv(wfname, index=False)
    # ============= end downloading and preprocessing data ==================
