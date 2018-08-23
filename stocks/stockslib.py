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
    time.sleep(10)

    return data


def get_last_prices(price=None, type='close', points=1):
    prices = price[map[type]].tail(points)
    return prices


def get_last_price(price=None, type='close'):
    prices = price[map[type]].tail(1)
    return prices.to_frame().iloc[0, 0]


def get_sma(pricedata=None, type='close', period=20, points=1):
    sma = pricedata[map[type]].rolling(window=period).mean()
    return sma.tail(points)


def get_sma_last(pricedata=None, type='close', period=20):
    sma = get_sma(pricedata=pricedata, type=type, period=period, points=1)
    sma = sma.to_frame().iloc[0, 0]
    return sma


def get_ema_last(pricedata=None, period=20):
    ema = technical_indicators.exponential_moving_average(pricedata.reset_index(), period)
    ema = ema.to_frame()
    ema = ema.tail(1).iloc[0, 0]
    return ema


def check_price_close_sma(type='close', period=20, prices=None):
    rez = 0
    buy_treshold = 2

    sma = get_sma_last(pricedata=prices, type=type, period=period)
    price = get_last_price(price=prices, type=type)

    if price > sma and abs(price/sma - 1) * 100 < buy_treshold:
        print('BUY: Price is close to SMA_' + str(period), price, sma)
        rez = 1
    return rez


def check_price_above_sma(type='close', period=50, prices=None):
    rez = 0

    sma = get_sma_last(pricedata=prices, type=type, period=period)
    price = get_last_price(price=prices, type=type)

    if price > sma:
        print('BUY: Price is above SMA_' + str(period), price, sma)
        rez = 1
    return rez


def check_price_above_ema(type='close', period=50, prices=None):
    rez = 0

    ema = get_ema_last(pricedata=prices, period=period)
    price = get_last_price(price=prices, type=type)

    if price > ema:
        print('BUY: Price is above EMA_' + str(period), price, ema)
        rez = 1
    return rez


def check_ema5_above_ema20(prices=None):
    ema5 = get_ema_last(pricedata=prices, period=5)
    ema20 = get_ema_last(pricedata=prices, period=20)

    if ema5 > ema20:
        print('BUY: EMA5 above EMA20 (shortterm bullish)', ema5, ema20)
        rez = 1
    else:
        print('Warning: EMA5 bellow EMA20', ema5, ema20)
        rez = -1

    return rez


def check_ema20_above_ema50(prices=None):
    ema20 = get_ema_last(pricedata=prices, period=20)
    ema50 = get_ema_last(pricedata=prices, period=50)

    if ema20 > ema50:
        print('BUY: EMA20 above EMA50 (midterm bullish)', ema20, ema50)
        rez = 1
    else:
        print('Warning: EMA20 bellow EMA50', ema20, ema50)
        rez = -1

    return rez


def check_sma20_above_sma100(prices=None):
    sma20 = get_sma_last(pricedata=prices, period=20)
    sma100 = get_sma_last(pricedata=prices, period=100)

    if sma20 > sma100:
        print('BUY: SMA20 above SMA100 (midterm bullish)', sma20, sma100)
        rez = 1
    else:
        print('Warning: SMA20 bellow SMA100', sma20, sma100)
        rez = -1

    return rez


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
    sell_treshold = 50
    for rsi in rsidata:
        if rsidata[rsi] < buy_treshold:
            print('BUY: RSI_' + str(period), rsi, rsidata[rsi])
            rez += 3

        if rsidata[rsi] > sell_treshold:
            print('Warning: RSI_' + str(period), rsi, rsidata[rsi])
            rez -= 2

    return rez


def check_rsi_sell(points=1, type='close', period=5, prices=None):
    rsidata = get_rsi(pricedata=prices, type=type, period=period, points=points)
    rez = 0
    sell_treshold = 65
    buy_treshold = 50
    for rsi in rsidata:
        if rsidata[rsi] > sell_treshold:
            print('SELL: RSI_' + str(period), rsi, rsidata[rsi])
            rez += 4

        if rsidata[rsi] < buy_treshold:
            print('Warning: RSI_' + str(period), rsi, rsidata[rsi])
            rez -= 2

    return rez


def check_macd(prices=None):
    """
    https://mindspace.ru/abcinvest/shozhdenie-rashozhdenie-skolzyashhih-srednih-moving-average-convergence-divergence-macd/
    https://mindspace.ru/abcinvest/aleksandr-elder-o-rashozhdeniyah-tseny-i-macd/
    https://mindspace.ru/30305-kak-ispolzovat-divergentsii-macd-dlya-vyyavleniya-razvorota-na-rynke/
    """
    data = technical_indicators.macd(prices.reset_index())
    data = data.set_index('date')
    macddata = data.tail(5).to_dict()

    last = None
    rez = 0
    grows = 0

    for macd_date in macddata['MACD_Hist']:
        macd_hist_value = macddata['MACD_Hist'][macd_date]
        if not last:
            last = macd_hist_value
            continue

        if last < 0 < macd_hist_value:
            print('BUY: MACD crossed signal line from DOWN', macd_date, last, macd_hist_value)
            rez += 4

        if last > 0 > macd_hist_value:
            print('Warning: MACD crossed signal line from UP', macd_date, last, macd_hist_value)
            rez -= 4
            
        if macd_hist_value > 0 and macddata['MACD'][macd_date] > 0:
            print('Short grows: MACD and Hist are positive', macd_date, macd_hist_value, macddata['MACD'][macd_date])
            grows = 1
        else:
            print('Warning: MACD and Hist are negative', macd_date, macd_hist_value, macddata['MACD'][macd_date])
            grows = -2

        last = macd_hist_value

    return rez + grows


