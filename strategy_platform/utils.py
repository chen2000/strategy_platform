from __future__ import absolute_import

import datetime

def strdate_add(strdate, days):
	t0 = datetime.datetime.strptime(strdate, '%Y-%m-%d')
	t = datetime.timedelta(days=days)
	t1 = t0 + t
	return t1.strftime('%Y-%m-%d')

def strdate_subtract(strdate, days):
	t0 = datetime.datetime.strptime(strdate, '%Y-%m-%d')
	t = datetime.timedelta(days=days)
	t1 = t0 - t
	return t1.strftime('%Y-%m-%d')
