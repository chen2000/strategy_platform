from __future__ import absolute_import

from strategy_platform.preprocess.preprocess import preprocess
from strategy_platform.preprocess.make_file import make_input_file, make_output_file
from strategy_platform.strategies.test_triggers import trigger_symbol_stats

import csv
import datetime
import os
import pandas as pd
import sys


start_date = '2007-01-01'
end_date = str(datetime.date.today())
trigger_start_date = str(datetime.date.today()-datetime.timedelta(14))
index = 'dow30'
source = 'quandl'	#yahoo or g_1year or quandl
a, b, success_window = 5, 2, 3

wdf = preprocess(source, index, start_date, end_date, force_rerun=True, force_rerun_ta=True)
# wdf = preprocess(source, index, start_date, end_date, force_rerun=False, force_rerun_ta=False)

# test rules per symbol
# e.g. GS, macd corss up, 5 consecutive neg values followed by 2 positive values

with open(make_input_file(index)) as csvfile:
    symbols = [row[0] for ind, row in enumerate(csv.reader(csvfile.read().splitlines())) if ind > 0]

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
df.Gain = pd.Series(["{0:.2f}%".format(val * 100) for val in df.Gain], index = df.index)
res_df.to_csv('data/results/accumulated_trigger_table.csv', sep=',', index=False)
#sent emails
os.system('cat data/results/accumulated_trigger_table.csv | mailx -s "Strategy Platform Trigger" \
         "lchen1688888@gmail.com, Fenhua.he@gmail.com, jianbin.he@gmail.com"')


# for symbol in symbols:
#     (stats_table, trigger_table) = trigger_symbol_stats_selling_strategy(symbol, index, a, b, success_window, up_rate, down_rate)

# res_show = pd.DataFrame()
# for symbol in symbols:
#     df = pd.read_csv(os.path.join(settings['folder']['results'], symbol + '_trigger_dates.csv'))
#     print(df.ix[df.Date>'2017-04-01', :])
#     res_show = pd.concat(res_show, df)

# test rules for all symbol in the index
#index_stats_table = trigger_index_stats(index, a, b, success_window)
