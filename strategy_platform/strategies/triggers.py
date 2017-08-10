from __future__ import absolute_import

from math import isnan
import os
import pandas as pd

from config.config import settings


def trigger_sporadic(symbol, index, success_window=None):
    trigger = []
    df = pd.read_csv(os.path.join(settings['folder']['trading'], index, symbol + '_ta.csv'))

    for i in xrange(df.shape[0] - success_window - 1):
        if df.ix[i, 'Close'] < df.ix[i+1, 'Close']:
            trigger.append(df.ix[i+1:i+1+success_window, ['Date', 'Close']])
    return trigger

def trigger_macd_trend(symbol, index, a, b, success_window=None):
    """
    a is num of days with macd diff neg
    b is num of days with macd diff pos
    success_window is num of days keeping track of price after trigger
    """
    trigger = []
    n = a + b
    df = pd.read_csv(os.path.join(settings['folder']['trading'], index, symbol + '_ta.csv'))

    for i in xrange(n, df.shape[0] - n - success_window):
        if isnan(df.ix[i, 'MACDdiff_12_26']):
            continue
        # during the period, MACD cannot be positive (has to be negative)
        if sum(df.ix[i:i+n-1, 'MACD_12_26'] > 0) > 0:
            continue
        # during the period, MACD cannot be larger than previous MACD low's 1/2
        if sum(df.ix[i:i+n-1, 'MACD_12_26'] < min(df.ix[max(i-200,0):i, 'MACD_12_26']) / 2) == 0:
            continue
        # a days negative diff and then b days positive diff
        if sum(df.ix[i:i+a-1, 'MACDdiff_12_26'] <=0) == a:
            if sum(df.ix[i+a:i+a+b-1, 'MACDdiff_12_26'] >=0) == b:
                trigger.append(df.ix[i+a+b:i+a+b+success_window, ['Date', 'MACD_12_26', 'MACDdiff_12_26', 'Close']])
    return trigger

def trigger_rsi_trend(symbol, index, a, b, success_window=None):
    """
    a is num of days with macd diff neg
    b is num of days with macd diff pos
    success_window is num of days keeping track of price after trigger
    """
    trigger = []
    n = a + b
    df = pd.read_csv(os.path.join(settings['folder']['trading'], index, symbol + '_ta.csv'))

    for i in xrange(n, df.shape[0] - n - success_window):
        if isnan(df.ix[i, 'RSI_14']):
            continue
        if sum(df.ix[i:i+a-1, 'RSI_14'] <=30) == a:
            if sum(df.ix[i+a:i+a+b-1, 'RSI_14'] >=30) == b:
                trigger.append(df.ix[i+a+b:i+a+b+success_window, ['Date', 'RSI_14', 'Close']])
    return trigger

def trigger_rsi_low(symbol, index, success_window=None):
    trigger = []
    df = pd.read_csv(os.path.join(settings['folder']['trading'], index, symbol + '_ta.csv'))
    for i in xrange(df.shape[0] - success_window):
        if isnan(df.ix[i, 'RSI_14']):
            continue
        if df.ix[i, 'RSI_14'] <= 30:
            trigger.append(df.ix[i:i+success_window, ['Date', 'RSI_14', 'Close']])
    return trigger

def trigger_rsi_high(symbol, index, success_window=None):
    trigger = []
    df = pd.read_csv(os.path.join(settings['folder']['trading'], index, symbol + '_ta.csv'))
    for i in xrange(df.shape[0] - success_window):
        if isnan(df.ix[i, 'RSI_14']):
            continue
        if df.ix[i, 'RSI_14'] >= 70:
            trigger.append(df.ix[i:i+success_window, ['Date', 'RSI_14', 'Close']])
    return trigger

def trigger_bband_upbreak(symbol, index, a, success_window=None):
    """
    a is num of days above mid of bband
    success_window is num of days keeping track of price after trigger
    """
    trigger = []
    df = pd.read_csv(os.path.join(settings['folder']['trading'], index, symbol + '_ta.csv'))

    for i in xrange(a, df.shape[0] - a - success_window):
        if isnan(df.ix[i, 'BollingerUpper20']):
            continue
        if sum(df.ix[i:i+a-1, 'Close'] >= df.ix[i:i+a-1, 'BollingerUpper20']) == a:
            trigger.append(df.ix[i+a:i+a+success_window, ['Date', 'BollingerUpper20', 'Close', 'MA_20']])
    return trigger

def trigger_bband_downbreak(symbol, index, a, success_window=None):
    """
    a is num of days above mid of bband
    success_window is num of days keeping track of price after trigger
    """
    trigger = []
    df = pd.read_csv(os.path.join(settings['folder']['trading'], index, symbol + '_ta.csv'))

    for i in xrange(a, df.shape[0] - a - success_window):
        if isnan(df.ix[i, 'BollingerLower20']):
            continue
        if sum(df.ix[i:i+a-1, 'Close'] <= df.ix[i:i+a-1, 'BollingerLower20']) == a:
            trigger.append(df.ix[i+a:i+a+success_window, ['Date', 'BollingerLower20', 'Close', 'MA_20']])
    return trigger

def trigger_bband_lowerflat(symbol, index, a, success_window=None):
    """
    a is num of days above mid of bband
    success_window is num of days keeping track of price after trigger
    after big drop, the bband lower band has to be flat to indicate stablized price and potential to a rebound
    """
    trigger = []
    df = pd.read_csv(os.path.join(settings['folder']['trading'], index, symbol + '_ta.csv'))

    for i in xrange(a, df.shape[0] - a - success_window):
        if isnan(df.ix[i, 'BollingerLower20']): # ignore the beginning time frame where there is no data
            continue
        rsnr = df.ix[i:i+a-1, 'BollingerLower20'].std()/df.ix[i:i+a-1, 'BollingerLower20'].mean()
        if rsnr < 0.01 and df.ix[i+a-1, 'Close'] >= df.ix[i, 'Close']:
            trigger.append(df.ix[i+a:i+a+success_window, ['Date', 'BollingerUpper20', 'Close', 'MA_20']])
    return trigger

def trigger_above_20wma(symbol, index, n, success_window=None):
    """
    If the symbol has been above 10 week ma for n weeks, trigger a buying signal.
    """
    trigger = []
    df = pd.read_csv(
            os.path.join(settings['folder']['trading'], index, symbol + '_weekly_ta.csv')
        )
    for i in xrange(n, df.shape[0] - n - success_window):
        if isnan(df.ix[i, 'MA_20']):
            continue    # ignore data at the beginning of time
        if sum(df.ix[i:i+n-1, 'MA_20'] - df.ix[i:i+n-1, 'Close'] < 0) == 0:
            trigger.append(df.ix[i+n:i+n+success_window, ['Date', 'MA_20', 'Close']])
    return trigger

def trigger_20wma_increase(symbol, index, n, success_window=None):
    """
    If the symbol has been above 10 week ma for n weeks, trigger a buying signal.
    """
    trigger = []
    df = pd.read_csv(
            os.path.join(settings['folder']['trading'], index, symbol + '_weekly_ta.csv')
        )
    for i in xrange(n, df.shape[0] - n - success_window - 1):
        if isnan(df.ix[i, 'MA_20']):
            continue    # ignore data at the beginning of time
        if sum(df.ix[i:i+n-1, 'MA_20'] - df.ix[i+1:i+n, 'MA_20'] > 0) == 0:
            trigger.append(df.ix[i+n:i+n+success_window, ['Date', 'MA_20', 'Close']])
    return trigger

def trigger_w_peak_touch(symbol, index, n, period, success_window=None):
    """
    If the symbol weekly close has touched peak n times during last "period" weeks
    """
    trigger = []
    df = pd.read_csv(
            os.path.join(settings['folder']['trading'], index, symbol + '_weekly_ta.csv')
        )
    for i in xrange(period, df.shape[0] - period - success_window):
        if isnan(df.ix[i, 'Close']):
            continue    # ignore data at the beginning of time
        if sum(df.ix[i:i+period, 'Close'] > df.ix[i:i+period, 'Close'].max()*0.99) > n:
            trigger.append(df.ix[i+period:i+period+success_window, ['Date', 'MA_20', 'Close']])
    return trigger
