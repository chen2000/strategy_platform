from __future__ import absolute_import, division

from collections import namedtuple
import csv

from strategy_platform.preprocess.yahoo_download import download_batch
from strategy_platform.preprocess.make_file import make_input_file, make_output_file


start_date = '1997-01-01'
end_date = '2017-01-15'
index = 'russel2000'

# load symbol name
with open(make_input_file(index)) as csvfile:
    symbols = [row[0] for ind, row in enumerate(csv.reader(csvfile)) if ind > 0]

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
