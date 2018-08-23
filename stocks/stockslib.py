"""
Stocks related stuff
"""

import pandas
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

map = dict()
map['close'] = '4. close'
map['low'] = '3. low'
map['high'] = '2. high'
map['open'] = '2. open'


def get_prices(symbol='', key=''):
    ts = TimeSeries(key=key, output_format='pandas')
    data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize='compact')
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
    up = delta * 0
    down = up.copy()
    up[delta > 0] = delta[delta > 0]
    down[delta < 0] = -delta[delta < 0]
    roll_up = up.rolling(window=period).mean()
    roll_down = down.rolling(window=period).mean()
    RS = roll_up / roll_down
    RSI = 100.0 - (100.0 / (1.0 + RS))

    return RSI.tail(points).to_dict()


def check_rsi(symbol='', key='', time=5, points=5, data=None):
    data = get_rsi(symbol='', key='', time=5)
    rsidata = data.tail(points).to_dict()

    buy_treshold = 35
    sell_treshold = 65
    for rsi in rsidata['RSI']:
        if rsidata['RSI'][rsi] < buy_treshold:
            print('BUY. RSI ' + str(time), rsi, rsidata['RSI'][rsi])

        if rsidata['RSI'][rsi] > sell_treshold:
            print('SELL. RSI ' + str(time), rsi, rsidata['RSI'][rsi])


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
