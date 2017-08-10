from __future__ import absolute_import

from collections import namedtuple
import csv

from strategy_platform.preprocess.yahoo_download import download_batch
from strategy_platform.preprocess.make_file import make_input_file, make_output_file


start_date = '1997-01-01'
end_date = '2017-01-15'
index = 'nasdaq100'

# load symbol name, note that nasdaq and sp500 has overlap, take overlap off nasdaq
with open(make_input_file('nasdaq100')) as csvfile:
    nasdaq100_symbols = [row[0] for ind, row in enumerate(csv.reader(csvfile.read().splitlines())) if ind > 0]
with open(make_input_file('sp500')) as csvfile:
    sp500_symbols = [row[0] for ind, row in enumerate(csv.reader(csvfile)) if ind > 0]
symbols = list(set(nasdaq100_symbols) - set(sp500_symbols))

# download trading data
daily_data = download_batch(
    symbols, 
    index, 
    start_date, 
    end_date, 
    'd', 
    make_output_file(index, 'daily'))

weekly_data = download_batch(
    symbols, 
    index, 
    start_date, 
    end_date, 
    'w', 
    make_output_file(index, 'weekly'))
