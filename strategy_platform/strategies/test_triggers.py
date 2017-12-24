from __future__ import absolute_import

from collections import namedtuple
import csv
import os

from config.config import settings
from strategy_platform.strategies import triggers
from strategy_platform.preprocess.make_file import make_input_file, make_output_file


Rule_stats = namedtuple('rule_stats', ['avg_gain', 'success_rate', 'frequency'])

def success_rate(trigger, success_window):
    # calculate stats of the rule, eg. success rate
    gain = 0
    success = 0
    for t in trigger:
        gain += float(t.reset_index().Close[success_window] - t.reset_index().Close[0]) / float(t.reset_index().Close[0])
        success += float(t.reset_index().Close[success_window] > t.reset_index().Close[0])

    frequency = len(trigger)
    if frequency == 0:
        avg_gain = None
        success_rate = None
    else:
        avg_gain = gain / float(frequency)
        success_rate = success / float(frequency)
    
    return Rule_stats._make([avg_gain, success_rate, frequency])

def success_rate_selling_strategy(trigger, success_window, up_rate, down_rate):
    # calculate stats of the rule, eg. success rate
    accumulated_gain = 0
    success, fail = 0, 0
    for t in trigger:
        close_values = t.Close
        initial_close = close_values.iloc[0]
        for i, cv in enumerate(close_values):
            if cv > initial_close * (1 + up_rate) or cv < initial_close * (1 - down_rate):
                break 
        gain = close_values.iloc[i] - initial_close
        if gain > 0:
            success += 1
        else:
            fail += 1
        accumulated_gain += gain
    frequency = len(trigger)
    success_rate = float(success) / (frequency + 0.0001)
    avg_gain = accumulated_gain / (frequency + 0.0001)
    # here frequency is total number tries, but success rate and avg_gain only counts success and fail, it does not count missing data, i.e. the upper/lower band is not hit
    return Rule_stats._make([avg_gain, success_rate, frequency])


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

    # weekly_success_window = 0
    # trigger = triggers.trigger_20wma_increase(symbol, index, 10, weekly_success_window)
    # stats = success_rate(trigger, weekly_success_window)
    # stats_table.append(['trigger_20wma_increase', symbol] + list(stats))
    # trigger_table += [['trigger_20wma_increase', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    with open(os.path.join(settings['folder']['results'], symbol + '_stats.csv'), 'wt') as csvfile:
        csv.writer(csvfile, delimiter=",").writerows(stats_table)
    with open(os.path.join(settings['folder']['results'], symbol + '_trigger_dates.csv'), 'wt') as csvfile:
        csv.writer(csvfile, delimiter=",").writerows(trigger_table)
    return (stats_table, trigger_table)


def trigger_symbol_stats_selling_strategy(symbol, index, a, b, success_window, up_rate, down_rate):
    """
    """

    stats_table = [['Trigger_name', 'Symbol', 'Avg_gain', 'Success_rate', 'Frequency']]
    trigger_table = [['Trigger_name', 'Symbol', 'Date', 'Gain']]

    trigger = triggers.trigger_sporadic(symbol, index, success_window)
    stats = success_rate(trigger, success_window)
    stats_table.append(['trigger_sporadic', symbol] + list(stats))

    trigger = triggers.trigger_macd_trend(symbol, index, a, b, success_window)
    stats = success_rate_selling_strategy(trigger, success_window, up_rate, down_rate)
    stats_table.append(['trigger_macd_trend', symbol] + list(stats))
    trigger_table += [['trigger_macd_trend', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_rsi_trend(symbol, index, a, b, success_window)
    stats = success_rate_selling_strategy(trigger, success_window, up_rate, down_rate)
    stats_table.append(['trigger_rsi_trend', symbol] + list(stats))
    trigger_table += [['trigger_rsi_trend', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_rsi_low(symbol, index, success_window)
    stats = success_rate_selling_strategy(trigger, success_window, up_rate, down_rate)
    stats_table.append(['trigger_rsi_low', symbol] + list(stats))
    trigger_table += [['trigger_rsi_low', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_rsi_high(symbol, index, success_window)
    stats = success_rate_selling_strategy(trigger, success_window, up_rate, down_rate)
    stats_table.append(['trigger_rsi_high', symbol] + list(stats))
    trigger_table += [['trigger_rsi_high', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_bband_lowerflat(symbol, index, a, success_window)
    stats = success_rate_selling_strategy(trigger, success_window, up_rate, down_rate)
    stats_table.append(['trigger_bband_lowerflat', symbol] + list(stats))
    trigger_table += [['trigger_bband_lowerflat', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_bband_upbreak(symbol, index, a, success_window)
    stats = success_rate_selling_strategy(trigger, success_window, up_rate, down_rate)
    stats_table.append(['trigger_bband_upbreak', symbol] + list(stats))
    trigger_table += [['trigger_bband_upbreak', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_bband_downbreak(symbol, index, a, success_window)
    stats = success_rate_selling_strategy(trigger, success_window, up_rate, down_rate)
    stats_table.append(['trigger_bband_downbreak', symbol] + list(stats))
    trigger_table += [['trigger_bband_downbreak', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    trigger = triggers.trigger_above_20wma(symbol, index, 10, 2)
    stats = success_rate_selling_strategy(trigger, success_window, up_rate, down_rate)
    stats_table.append(['trigger_above_20wma', symbol] + list(stats))
    trigger_table += [['trigger_above_20wma', symbol, ele.iloc[0].Date, (ele.iloc[-1].Close-ele.iloc[0].Close)/ele.iloc[0].Close] for ele in trigger]

    with open(os.path.join(settings['folder']['results'], symbol + '_selling_strategy_stats.csv'), 'wt') as csvfile:
        csv.writer(csvfile, delimiter=",").writerows(stats_table)
    with open(os.path.join(settings['folder']['results'], symbol + '_selling_strategy_trigger_dates.csv'), 'wt') as csvfile:
        csv.writer(csvfile, delimiter=",").writerows(trigger_table)
    return (stats_table, trigger_table)


def trigger_index_stats(index, a, b, success_window):
    with open(make_input_file(index)) as csvfile:
        symbols = [row[0] for ind, row in enumerate(csv.reader(csvfile.read().splitlines())) if ind > 0]

    stats_table = [['Trigger_name', 'Index', 'Avg_gain', 'Success_rate', 'Frequency']]

    weighted_gain = weighted_rate = cnt = 0
    for symbol in symbols:
        trigger = triggers.trigger_sporadic(symbol, index, success_window)
        stats = success_rate(trigger, success_window)
        weighted_gain += stats.avg_gain * stats.frequency
        weighted_rate += stats.success_rate * stats.frequency
        cnt += stats.frequency
    stats_table.append(['trigger_sporadic', index, weighted_gain/cnt, weighted_rate/cnt, cnt])
 
    weighted_gain = weighted_rate = cnt = 0
    for symbol in symbols:
        trigger = triggers.trigger_macd_trend(symbol, index, a, b, success_window)
        stats = success_rate(trigger, success_window)
        weighted_gain += stats.avg_gain * stats.frequency
        weighted_rate += stats.success_rate * stats.frequency
        cnt += stats.frequency
    stats_table.append(['trigger_macd_trend', index, weighted_gain/cnt, weighted_rate/cnt, cnt])

    weighted_gain = weighted_rate = cnt = 0
    for symbol in symbols:
        trigger = triggers.trigger_rsi_trend(symbol, index, a, b, success_window)
        stats = success_rate(trigger, success_window)
        weighted_gain += stats.avg_gain * stats.frequency
        weighted_rate += stats.success_rate * stats.frequency
        cnt += stats.frequency
    stats_table.append(['trigger_rsi_trend', index, weighted_gain/cnt, weighted_rate/cnt, cnt])

    weighted_gain = weighted_rate = cnt = 0
    for symbol in symbols:
        trigger = triggers.trigger_rsi_low(symbol, index, success_window)
        stats = success_rate(trigger, success_window)
        weighted_gain += stats.avg_gain * stats.frequency
        weighted_rate += stats.success_rate * stats.frequency
        cnt += stats.frequency
    stats_table.append(['trigger_rsi_low', index, weighted_gain/cnt, weighted_rate/cnt, cnt])

    weighted_gain = weighted_rate = cnt = 0
    for symbol in symbols:
        trigger = triggers.trigger_rsi_high(symbol, index, success_window)
        stats = success_rate(trigger, success_window)
        weighted_gain += stats.avg_gain * stats.frequency
        weighted_rate += stats.success_rate * stats.frequency
        cnt += stats.frequency
    stats_table.append(['trigger_rsi_high', index, weighted_gain/cnt, weighted_rate/cnt, cnt])

    weighted_gain = weighted_rate = cnt = 0
    for symbol in symbols:
        trigger = triggers.trigger_bband_lowerflat(symbol, index, a, success_window)
        stats = success_rate(trigger, success_window)
        weighted_gain += stats.avg_gain * stats.frequency
        weighted_rate += stats.success_rate * stats.frequency
        cnt += stats.frequency
    stats_table.append(['trigger_bband_lowerflat', index, weighted_gain/cnt, weighted_rate/cnt, cnt])

    weighted_gain = weighted_rate = cnt = 0
    for symbol in symbols:
        trigger = triggers.trigger_bband_upbreak(symbol, index, a, success_window)
        stats = success_rate(trigger, success_window)
        weighted_gain += stats.avg_gain * stats.frequency
        weighted_rate += stats.success_rate * stats.frequency
        cnt += stats.frequency
    stats_table.append(['trigger_bband_upbreak', index, weighted_gain/cnt, weighted_rate/cnt, cnt])

    weighted_gain = weighted_rate = cnt = 0
    for symbol in symbols:
        trigger = triggers.trigger_bband_downbreak(symbol, index, a, success_window)
        stats = success_rate(trigger, success_window)
        weighted_gain += stats.avg_gain * stats.frequency
        weighted_rate += stats.success_rate * stats.frequency
        cnt += stats.frequency
    stats_table.append(['trigger_bband_downbreak', index, weighted_gain/cnt, weighted_rate/cnt, cnt])

    weighted_gain = weighted_rate = cnt = 0
    for symbol in symbols:
        trigger = triggers.trigger_above_20wma(symbol, index, 10, 2)    # weekly data has n=10, successwindow=2, different from daily data
        stats = success_rate(trigger, success_window)
        weighted_gain += stats.avg_gain * stats.frequency
        weighted_rate += stats.success_rate * stats.frequency
        cnt += stats.frequency
    stats_table.append(['trigger_above_20wma', index, weighted_gain/cnt, weighted_rate/cnt, cnt])

    with open(os.path.join(settings['folder']['results'], index + '_results.csv'), 'wt') as csvfile:
        csv.writer(csvfile, delimiter=",").writerows(stats_table)
    return stats_table
