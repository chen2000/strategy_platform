from __future__ import absolute_import

import numpy  
import pandas as pd  
import math as m


#Moving Average  
def ma(df, n):  
    MA = pd.Series(pd.rolling_mean(df['Close'], n), name = 'MA_' + str(n))  
    df = df.join(MA)  
    return df

#Exponential Moving Average  
def ema(df, n):  
    EMA = pd.Series(pd.ewma(df['Close'], span = n, min_periods = n - 1), name = 'EMA_' + str(n))  
    df = df.join(EMA)  
    return df

#Bollinger Bands  
def b_bands(df, n):  
    MA = pd.Series(pd.rolling_mean(df['Close'], n))  
    MSD = pd.Series(pd.rolling_std(df['Close'], n))
    upper = pd.Series(MA + MSD * 2, name = 'BollingerUpper' + str(n))  
    df = df.join(upper)
    lower = pd.Series(MA - MSD * 2, name = 'BollingerLower' + str(n))
    df = df.join(lower)
    return df

def rsi(df, n):  
    price = df.ix[:, 'Close'].tolist()
    price_len = len(price)
    rsi_l = [None] * price_len
    for i in xrange(n, price_len):
        t0 = price[i-n:i]
        t1 = price[i-n+1:i+1]
        hist_diff = [t1[j] - t0[j] for j in xrange(n)]    # track back to 13 days ago to today
        gain, loss = 0, 0
        for ele in hist_diff:   
            if ele >= 0:
                gain += ele
            else:
                loss += -ele    # loss needs abs value
        rs = float(gain) / (loss + 1e-6)
        rsi_l[i] = 100.0 - 100.0 / (1 + rs)
    df = pd.concat([df, pd.DataFrame({'RSI_' + str(n): rsi_l})], axis=1)
    return df

#MACD, MACD Signal and MACD difference  
def macd(df, n_fast, n_slow):  
    EMAfast = pd.Series(pd.ewma(df['Close'], span = n_fast, min_periods = n_fast - 1))
    EMAslow = pd.Series(pd.ewma(df['Close'], span = n_slow, min_periods = n_slow - 1))
    MACD = pd.Series(EMAfast - EMAslow, name = 'MACD_' + str(n_fast) + '_' + str(n_slow))
    MACDsign = pd.Series(pd.ewma(MACD, span = 9, min_periods = 8), name = 'MACDsign_' + str(n_fast) + '_' + str(n_slow))
    MACDdiff = pd.Series(MACD - MACDsign, name = 'MACDdiff_' + str(n_fast) + '_' + str(n_slow))
    df = df.join(MACD)
    df = df.join(MACDsign)
    df = df.join(MACDdiff)
    return df


#Stochastic oscillator %K  
def sto_k(df, n):  
    high_n = pd.rolling_max(df['High'], n)
    low_n = pd.rolling_min(df['Low'], n)
    SOk = pd.Series( 100 * (df['Close'] - low_n) / (high_n - low_n), name = 'SO%k' + str(n))  
    df = df.join(SOk)  
    return df

#Stochastic oscillator %D  
def sto_d(df, n):  
    high_n = pd.rolling_max(df['High'], n)
    low_n = pd.rolling_min(df['Low'], n)
    SOk = pd.Series( 100 * (df['Close'] - low_n) / (high_n - low_n), name = 'SO%k')  
    SOd = pd.Series(pd.rolling_mean(SOk, 3), name = 'SO%d' + str(n))  
    df = df.join(SOd)  
    return df
