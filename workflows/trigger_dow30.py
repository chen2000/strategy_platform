from __future__ import absolute_import

from strategy_platform.preprocess.preprocess import preprocess
from strategy_platform.preprocess.make_file import make_input_file, make_output_file
from strategy_platform.strategies.test_triggers import trigger_symbol_stats

import csv
import datetime
import os
import pandas as pd
import sys


index = 'dow30'
source = 'quandl'
today = datetime.date.today()
start_date = str(today-datetime.timedelta(365))
end_date = str(today)
trigger_start_date = str(today-datetime.timedelta(14))
a, b, success_window = 5, 2, 0 	# success_window=0 for forecast realtime
# a and b is for particular trigger, e.g. GS, macd corss up, 5 consecutive neg values followed by 2 positive values

# load symbols
with open(make_input_file(index)) as csvfile:
    symbols = [row[0] for ind, row in enumerate(csv.reader(csvfile.read().splitlines())) if ind > 0]

# get recent data and ta indicators
preprocess(source, index, start_date, end_date, force_rerun=True, force_rerun_ta=True)

# apply trigger based on ta indicators
accumulated_trigger_table = []
for ind, symbol in enumerate(symbols):
    (stats_table, trigger_table) = trigger_symbol_stats(symbol, index, a, b, success_window)
    if ind == 0:
        accumulated_trigger_table += trigger_table
    else:
        accumulated_trigger_table += trigger_table[1:]

# reformat res and save as csv
df = pd.DataFrame(accumulated_trigger_table[1:], columns=accumulated_trigger_table[0])
res_df = df.loc[df.Date > trigger_start_date]
res_df[res_df['Trigger_name'] == 'trigger_macd_trend'].to_csv('data/dow30_MACD_trigger_table.csv', sep=',', index=False)

#sent emails
os.system('cat data/dow30_MACD_trigger_table.csv | mailx -s "Strategy Platform Trigger" \
         lchen1688888@gmail.com Fenhua.he@gmail.com jianbin.he@gmail.com fenhua_he@yahoo.com')
