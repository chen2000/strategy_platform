from __future__ import absolute_import, division

from collections import namedtuple
import csv
import time
import datetime
import subprocess
import StringIO
import urllib2


targeted_format = ['Symbol', 'Date', 'High', 'Low', 'Open', 'Close', 'Adj_Close', 'Volume']
yahoo_targeted_map = [1, 4, 2, 3, 5, 7, 6]
g_1year_targeted_map = {1:0, 2:2, 3:3, 4:1, 5:4, 6:4, 7:5}
quandl_targeted_map = {1:0, 2:2, 3:3, 4:1, 5:4, 6:11, 7:5}
TimeSeg = namedtuple('TimeSeg', ['year', 'month', 'date'])

def csvstr_ll(scsv):
	"""
	Convert string of csv format to list of list
	"""
	f = StringIO.StringIO(scsv)
	reader = csv.reader(f, delimiter=',')
	return [row for row in reader]

def make_url(source, symbol, start_date, end_date, frequency='d'):
	"""
	Use yahoo or google url to download trading data
	frequency in ('w', 'd') denoting weekly or daily
	dates are strings in YYYY-MM-DD format
	"""
	def parse_time_str(time_str):
		"""
		time_str follows 'YYYY-MM-DD'
		"""		
		year, month, date = time_str[:4], time_str[5:7], time_str[8:]
		return TimeSeg._make([year, month, date])

	def str_bigint(time_str):
		return int(time.mktime(datetime.datetime.strptime(time_str, "%Y-%m-%d").timetuple()))

	if source == 'yahoo':
		start_date_seg = parse_time_str(start_date)
		end_date_seg = parse_time_str(end_date)
		url = "http://chart.finance.yahoo.com/table.csv?s={symbol}&a={month0}&b={date0}&c={year0}&d={month1}&e={date1}&f={year1}&g={frequency}&ignore=.csv"\
			.format(
				symbol=symbol, 
				month0=start_date_seg.month,
				date0=start_date_seg.date,
				year0=start_date_seg.year,
				month1=end_date_seg.month,
				date1=end_date_seg.date,
				year1=end_date_seg.year,
				frequency=frequency)
	elif source == 'g_1year':
		url = "https://www.google.com/finance/historical?output=csv&q={symbol}"\
			.format(symbol=symbol)
	elif source == 'quandl':
		url = "https://www.quandl.com/api/v3/datasets/WIKI/{symbol}/data.csv?&start_date={start_date}&end_date={end_date}&collapse=daily&api_key=QsLx85TxiSx6zD_spWGh"\
			.format(symbol=symbol, start_date=start_date, end_date=end_date)
	else:
		raise NameError('Not an exisisting source!')
	return url

def retry_download(source, symbol, start_date, end_date, frequency='d'):
	retry_max, retry_cnt = 3, 0
	while True:
		if retry_cnt == retry_max:
			print('"{symbol}" failed 3 times... skip'.format(symbol=symbol))
			retry_cnt = 0
			return []
		try:
			url = make_url(source, symbol, start_date, end_date, frequency)
			if source == 'yahoo':
				response = urllib2.urlopen(url)
				data = [row for row in csv.reader(response)][1:]	# skip header
			elif source in ('g_1year', 'quandl'):
				response = subprocess.check_output("curl \'" + url + "\'", shell=True)
				data = csvstr_ll(response)[1:]
			else:
				raise NameError('Non-existent source!')
			print('"{symbol}" downloaded...'.format(symbol=symbol))
		except urllib2.HTTPError:
			print('"{symbol}" cannot be downloaded...'.format(symbol=symbol))
			retry_cnt += 1
			continue
		except Exception as e:
			print('"{symbol}" met other exceptions...:'.format(symbol=symbol) + str(e))
			retry_cnt += 1
			continue
		break
	return data

def download_batch(source, symbols, batch_name, start_date, end_date, frequency, output_file):

	def download_helper(source_map):
		trading_csv = []
		for symbol in symbols:
			trading_raw = retry_download(source, symbol, start_date, end_date)
			for row in trading_raw:
				csv_row = [symbol] + [None] * len(source_map)
				for i in source_map:
					csv_row[i] = row[source_map[i]]
				trading_csv.append(csv_row)
		trading_csv.insert(0, targeted_format)
		return trading_csv

	if source == 'g_1year':
		trading_csv = download_helper(g_1year_targeted_map)
	elif source == 'quandl':
		trading_csv = download_helper(quandl_targeted_map)
	else:
		raise NameError('Source batch download is not built until source is confirmed reliable')
	with open(output_file, 'wt') as csvfile:
		csv.writer(csvfile, delimiter=',').writerows(trading_csv)
