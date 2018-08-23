"""
Stocks related stuff
"""

import numpy as np
import time
import sys
import os
# sys.path.insert(0, os.path.abspath('..'))
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import technical_indicators
from pprint import pprint

map = dict()
map['close'] = '4. close'
map['low'] = '3. low'
map['high'] = '2. high'
map['open'] = '2. open'


def get_prices(symbol='', key='', cachedir='cache', cacheage=3600*8):
    if not os.path.isdir(cachedir):
        os.mkdir(cachedir)
    filename = symbol + '.csv'
    filepath = os.path.join(cachedir, filename)
    if os.path.isfile(filepath):
        age = time.time() - os.path.getmtime(filepath)
        if age > cacheage:
            os.remove(filepath)
        else:
            data = pd.read_csv(filepath, index_col='date')
            return data

    ts = TimeSeries(key=key, output_format='pandas')
    data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize='compact')
    data.to_csv(filepath)

    return data


def get_last_prices(pricedata=None, type='close', points=5):
    prices = pricedata[map[type]].tail(points).to_dict()
    return prices


def get_sma(pricedata=None, type='close', period=20, points=5):
    sma = pricedata[map[type]].rolling(window=period).mean()
    return sma.tail(points).to_dict()


def get_rsi(pricedata=None, type='close', period=5, points=5):
    """https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas"""
    data = pricedata[map[type]]

    delta = data.diff().dropna()

    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    roll_up = up.rolling(window=period).mean()
    roll_down = down.abs().rolling(window=period).mean()

    rs = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + rs))

    return rsi.tail(points).to_dict()


def get_rsi2(pricedata=None, period=5, points=5):
    """https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas"""
    rsi2 = technical_indicators.relative_strength_index(pricedata.reset_index(), period)

    return rsi2.tail(points).to_dict()


def check_rsi(points=1, type='close', period=5, prices=None):
    rsidata = get_rsi(pricedata=prices, type=type, period=period, points=points)
    rez = 0
    buy_treshold = 35
    for rsi in rsidata:
        if rsidata[rsi] < buy_treshold:
            print('BUY. RSI ' + str(time), rsi, rsidata[rsi])
            rez = 1

    return rez


def check_rsi_sell(points=1, type='close', period=5, prices=None):
    rsidata = get_rsi(pricedata=prices, type=type, period=period, points=points)
    rez = 0
    sell_treshold = 65
    for rsi in rsidata:
        if rsidata[rsi] > sell_treshold:
            print('SELL. RSI ' + str(time), rsi, rsidata[rsi])
            rez = 1

    return rez


def check_macd(symbol='', key='', interval='daily', points=5):
    """
    https://mindspace.ru/abcinvest/shozhdenie-rashozhdenie-skolzyashhih-srednih-moving-average-convergence-divergence-macd/
    https://mindspace.ru/abcinvest/aleksandr-elder-o-rashozhdeniyah-tseny-i-macd/
    https://mindspace.ru/30305-kak-ispolzovat-divergentsii-macd-dlya-vyyavleniya-razvorota-na-rynke/
    """
    ti = TechIndicators(key=key, output_format='pandas')
    data, meta_data = ti.get_macd(symbol=symbol, interval=interval)
    macddata = data.tail(points).to_dict()
    last = None
    for macd_date in macddata['MACD_Hist']:
        macd_hist_value = macddata['MACD_Hist'][macd_date]
        if not last:
            last = macd_hist_value
            continue

        if last < 0 and macd_hist_value > 0:
            print('MACD crossed on ' + interval, macd_date, last, macd_hist_value)
            
        if macd_hist_value > 0 and macddata['MACD'][macd_date] > 0:
            print('Short grow: MACD and Hist are positive on ' + interval, macd_date, macd_hist_value, macddata['MACD'][macd_date])

        last = macd_hist_value
