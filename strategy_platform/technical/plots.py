from __future__ import absolute_import

import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2
import os
import pandas as pd

from config.config import settings


def create_ta_charts(symbol, index, start_date, end_date, s_start_date, s_end_date):
    """
    Give symbol and time period, automatically locate file, read data and plot
    """
    batch = symbol + '_' + s_start_date + s_end_date
    p_dir = os.path.join(settings['folder']['plots'], index)
    if not os.path.exists(p_dir):
        os.mkdir(p_dir)
    df = pd.read_csv(os.path.join(settings['folder']['trading'], index, symbol + '_ta.csv'))
    df['Date'] = pd.to_datetime(df['Date'])
    df_show = df[(df['Date'] >= s_start_date) & (df['Date'] <= s_end_date)].reset_index().drop('index', axis=1)
    plot_technical(df_show, os.path.join(p_dir, batch + '_technical.png'), show_option=False)
    plot_candlestick(df_show, os.path.join(p_dir, batch + '_candlestick.png'), show_option=False)


def plot_technical(df_show, save_file, show_option=False):
    show_days = df_show.shape[0]
    plt.close('all')
    f, axarr = plt.subplots(7, sharex=True)
    axarr[0].plot(df_show.Date, df_show[['Close', 'MA_20', 'MA_50']])
    axarr[0].set_title("MA", fontsize=8)
    axarr[1].plot(df_show.Date, df_show[['Close', 'MA_20', 'BollingerUpper20', 'BollingerLower20']])
    axarr[1].set_title("Bollinger", fontsize=8)
    axarr[2].plot(df_show.Date, df_show[['Volume']])
    axarr[2].set_title("Volume", fontsize=8)
    axarr[3].plot(df_show.Date, df_show[['RSI_14']])
    axarr[3].set_title("RSI", fontsize=8)
    axarr[4].plot(df_show.Date, df_show[['MACD_12_26']], color='b')
    axarr[4].plot(df_show.Date, df_show[['MACDsign_12_26']], color='r')
    axarr[4].set_title("MACD", fontsize=8)
    axarr[5].plot(df_show.Date, df_show[['MACDdiff_12_26']], 'o-')
    axarr[5].plot(df_show.Date, pd.DataFrame({'zero': [0] * show_days}))
    axarr[5].set_title("MACD_diff", fontsize=8)
    axarr[6].plot(df_show.Date, df_show[['SO%k14']], color='b')
    axarr[6].plot(df_show.Date, df_show[['SO%d14']], color='r')
    axarr[6].set_title("Stochastic", fontsize=8)
    #plt.xlim(0, show_days) # plt does not allow xlim if x is timestamp
    f.set_size_inches(12, 8)
    f.savefig(save_file)
    if show_option:
        plt.show()

def plot_candlestick(df_show, save_file, show_option=False):
    show_days = df_show.shape[0]
    plt.close('all')
    f, axarr = plt.subplots(3, sharex=True)
    axarr[0].plot(range(show_days), df_show[['MA_20', 'MA_50']])
    candlestick2(axarr[0], df_show.Open, df_show.Close, df_show.High, df_show.Low, width=1, colorup='g', colordown='r', alpha=0.75)
    axarr[1].plot(range(show_days), df_show[['Close', 'MA_20', 'BollingerUpper20', 'BollingerLower20']])
    candlestick2(axarr[1], df_show.Open, df_show.Close, df_show.High, df_show.Low, width=1, colorup='g', colordown='r', alpha=0.75)
    axarr[2].plot(range(show_days), df_show[['Volume']])
    axarr[2].set_title("Volume", fontsize=8)
    plt.xlim(0, show_days)
    f.set_size_inches(12, 8)
    f.savefig(save_file)
    if show_option:
        plt.show()
