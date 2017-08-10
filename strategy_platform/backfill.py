from __future__ import absolute_import, division

from collections import namedtuple
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from strategy_platform.scripts import load_price
from strategy_platform.models.metrics.price import DailyPrice, WeeklyPrice
import logging


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)
"""
need to revisit kafka logging
_logger = config.get_logger('arnold.scripts.load_dictionary')
"""

if __name__ == '__main__':
    """
    to replace ind list by config
    """

    Price = namedtuple('Price', [
        'index',
        'symbol', 
        'date', 
        'high', 
        'low', 
        'open',
        'close',
        'volume',
    ])
    
    # for index in ['dow30', 'sp500', 'nasdaq100', 'russell2000']:
    for index in ['russell2000']:
        # loading daily data
        df = pd.read_csv('data/' + index + '_d_trading.csv')
        df = df.drop_duplicates(subset=['Symbol', 'Date'])
        prices = [Price(
            index, 
            row.Symbol,
            row.Date,
            row.High,
            row.Low,
            row.Open,
            row.Close,
            row.Volume,
        ) for i, row in df.iterrows()]
        load_price.load_price(prices, DailyPrice)

        # loading weekly data
        df = pd.read_csv('data/' + index + '_w_trading.csv')
        df = df.drop_duplicates(subset=['Symbol', 'Date'])
        prices = [Price(
            index, 
            row.Symbol,
            row.Date,
            row.High,
            row.Low,
            row.Open,
            row.Close,
            row.Volume,
        ) for i, row in df.iterrows()]
        load_price.load_price(prices, WeeklyPrice)
