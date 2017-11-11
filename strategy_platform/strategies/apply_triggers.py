from __future__ import absolute_import

from collections import namedtuple
import csv
import os

from config.config import settings
from strategy_platform.strategies import triggers
from strategy_platform.preprocess.make_file import make_input_file, make_output_file


Rule_stats = namedtuple('rule_stats', ['avg_gain', 'success_rate', 'frequency'])

def trigger_symbol_stats(symbol, index, a, b, success_window):
    """
    """

    stats_table = [['Trigger_name', 'Symbol', 'Avg_gain', 'Success_rate', 'Frequency']]
    trigger_table = [['Trigger_name', 'Symbol', 'Date', 'Gain']]

    trigger = triggers.trigger_sporadic(symbol, index, success_window)
    stats = success_rate(trigger, success_window)
    stats_table.append(['trigger_sporadic', symbol] + list(stats))

    trigger = triggers.trigger_macd_trend(symbol, index, a, b, success_window)
    stats = success_rate(trigger, success_window)
    stats_table.append(['trigger_macd_trend', symbol] + list(stats))
    trigger_table += [['trigger_macd_trend', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_rsi_trend(symbol, index, a, b, success_window)
    stats = success_rate(trigger, success_window)
    stats_table.append(['trigger_rsi_trend', symbol] + list(stats))
    trigger_table += [['trigger_rsi_trend', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_rsi_low(symbol, index, success_window)
    stats = success_rate(trigger, success_window)
    stats_table.append(['trigger_rsi_low', symbol] + list(stats))
    trigger_table += [['trigger_rsi_low', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_rsi_high(symbol, index, success_window)
    stats = success_rate(trigger, success_window)
    stats_table.append(['trigger_rsi_high', symbol] + list(stats))
    trigger_table += [['trigger_rsi_high', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_bband_lowerflat(symbol, index, a, success_window)
    stats = success_rate(trigger, success_window)
    stats_table.append(['trigger_bband_lowerflat', symbol] + list(stats))
    trigger_table += [['trigger_bband_lowerflat', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_bband_upbreak(symbol, index, a, success_window)
    stats = success_rate(trigger, success_window)
    stats_table.append(['trigger_bband_upbreak', symbol] + list(stats))
    trigger_table += [['trigger_bband_upbreak', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_bband_downbreak(symbol, index, a, success_window)
    stats = success_rate(trigger, success_window)
    stats_table.append(['trigger_bband_downbreak', symbol] + list(stats))
    trigger_table += [['trigger_bband_downbreak', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    weekly_success_window = 0
    trigger = triggers.trigger_20wma_increase(symbol, index, 10, weekly_success_window)
    stats = success_rate(trigger, weekly_success_window)
    stats_table.append(['trigger_20wma_increase', symbol] + list(stats))
    trigger_table += [['trigger_20wma_increase', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    with open(os.path.join(settings['folder']['results'], symbol + '_stats.csv'), 'wt') as csvfile:
        csv.writer(csvfile, delimiter=",").writerows(stats_table)
    with open(os.path.join(settings['folder']['results'], symbol + '_trigger_dates.csv'), 'wt') as csvfile:
        csv.writer(csvfile, delimiter=",").writerows(trigger_table)
    return (stats_table, trigger_table)
