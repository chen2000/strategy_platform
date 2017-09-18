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

def make_url(source, symbol, start_date='2017-01-01', end_date='2017-01-02', frequency='d'):
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
		# url = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval=1d&events=history&crumb=8vzabQ7f0ah"\
		# 	.format(
		# 		symbol=symbol,
		# 		period1=str_bigint(start_date),
		# 		period2=str_bigint(end_date))
	elif source == 'g_realtime':	# still not figured out how to use it
		# trange has to prorate 5/7 since this g finance only counts trading dates
		trange = (time.mktime(datetime.datetime.now().timetuple())-str_bigint(start_date))/86400*5/7
		print('Google Finance only provides start date to today, no end_date')
		if frequency == 'w':
			period = 86400 * 5
		else:
			period = 86400
		url = "https://www.google.com/finance/getprices?i={period}&p={trange}d&f=d,o,h,l,c,v&df=cpct&q={symbol}"\
			.format(period=period, trange=trange, symbol=symbol)
	elif source == 'g_1year':
		# g 1 year only gives current 1 year data
		url = "https://www.google.com/finance/historical?output=csv&q={symbol}"\
			.format(symbol=symbol)
	elif source == 'quandl':
		url = "https://www.quandl.com/api/v3/datasets/WIKI/{symbol}/data.csv?api_key=QsLx85TxiSx6zD_spWGh"\
			.format(symbol=symbol)
	else:
		raise NameError('Not an exisisting source!')
	return url

def retry_download(source, symbol, start_date='2017-01-01', end_date='2017-01-02', frequency='d'):
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
			elif source == 'g_realtime':
				response = subprocess.check_output("curl \'" + url + "\'", shell=True)
				data = response[7:]
			elif source == 'g_1year':
				response = subprocess.check_output("curl \'" + url + "\'", shell=True)
				data = csvstr_ll(response)[1:]
			elif source == 'quandl':
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
			# show uncaptured exceptions
			print('"{symbol}" met other exceptions...:'.format(symbol=symbol) + str(e))
			retry_cnt += 1
			continue
		break
	return data

def download_batch(source, symbols, batch_name, start_date, end_date, frequency, output_file):
	# Note: need to transfrom yahoo_http_format as yahoo_api_format
	if source == 'g_1year':
		# to avoid overwrite yahoo long hist data by g 1 year data
		output_file = output_file[:-5] + "_g_1year.csv"
		trading_csv = []
		for symbol in symbols:
			trading_raw = retry_download(source, symbol)
			for row in trading_raw:
				csv_row = [symbol] + [None] * len(g_1year_targeted_map)
				for i in g_1year_targeted_map:
					csv_row[i] = row[g_1year_targeted_map[i]]
				trading_csv.append(csv_row)
		trading_csv.insert(0, targeted_format)
	elif source == 'yahoo':
		trading_csv = []
		for symbol in symbols:
			trading_raw = retry_download(source, symbol, start_date, end_date, frequency)
			for row in trading_raw:
				csv_row = [symbol] + [None] * len(yahoo_targeted_map)
				for i in xrange(len(yahoo_targeted_map)):
					csv_row[yahoo_targeted_map[i]] = row[i]
				trading_csv.append(csv_row)
		trading_csv.insert(0, targeted_format)
	elif source == 'quandl':
		# to avoid overwrite yahoo and google  data by quandl data
		output_file = output_file[:-5] + "_quandl.csv"
		trading_csv = []
		for symbol in symbols:
			trading_raw = retry_download(source, symbol)
			for row in trading_raw:
				csv_row = [symbol] + [None] * len(quandl_targeted_map)
				for i in quandl_targeted_map:
					csv_row[i] = row[quandl_targeted_map[i]]
				trading_csv.append(csv_row)
		trading_csv.insert(0, targeted_format)
	else:
		raise NameError('Source batch download is not built until source is confirmed reliable')
	with open(output_file, 'wt') as csvfile:
		csv.writer(csvfile, delimiter=',').writerows(trading_csv)
