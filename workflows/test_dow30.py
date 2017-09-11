from __future__ import absolute_import

from strategy_platform.preprocess.preprocess import preprocess
from strategy_platform.preprocess.make_file import make_input_file, make_output_file
from strategy_platform.strategies.test_triggers import trigger_symbol_stats

import csv
import os
import sys
import time


start_date = '2007-01-01'
end_date = time.strftime("%Y-%m-%d")
index = 'dow30'
source = 'g_1year'	#yahoo or g_1year


wdf = preprocess(source, index, start_date, end_date, force_rerun=True, force_rerun_ta=True)
wdf = preprocess(source, index, start_date, end_date, force_rerun=False, force_rerun_ta=False)

a, b, success_window = 5, 2, 3
# test rules per symbol
# e.g. GS, macd corss up, 5 consecutive neg values followed by 2 positive values

with open(make_input_file(index)) as csvfile:
    symbols = [row[0] for ind, row in enumerate(csv.reader(csvfile.read().splitlines())) if ind > 0]

accumulated_trigger_table = []
for symbol in symbols:
    (stats_table, trigger_table) = trigger_symbol_stats(symbol, index, a, b, success_window)
    accumulated_trigger_table += trigger_table
with open('data/results/accumulated_trigger_table.csv', 'wt') as csvfile:
    csv.writer(csvfile, delimiter=",").writerows(accumulated_trigger_table)

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
