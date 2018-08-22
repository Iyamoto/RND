"""
Checks for good buy options
"""

import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time
import alphaconf

key = alphaconf.key


def check_rsi(symbol='', key='', time=5, treshold=65, points=5):
    ti = TechIndicators(key=key, output_format='pandas')
    data, meta_data = ti.get_rsi(symbol=symbol, time_period=time)
    rsidata = data.tail(points).to_dict()
    for rsi in rsidata['RSI']:
        if rsidata['RSI'][rsi] > treshold:
            print('RSI ' + str(time), rsi, rsidata['RSI'][rsi])


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

        if last > 0 and macd_hist_value < 0:
            print('MACD crossed on ' + interval, macd_date, last, macd_hist_value)
            
        last = macd_hist_value


# Lets start

for symbol in alphaconf.symbols2sell:
    print('====')
    print(symbol)

    try:
        # Check RSI
        check_rsi(symbol=symbol, key=alphaconf.key, time=5)
        # check_rsi(symbol=symbol, key=alphaconf.key, time=14)

        time.sleep(5)

        # Check MACD
        check_macd(symbol=symbol, key=alphaconf.key)
        # check_macd(symbol=symbol, key=alphaconf.key, interval='weekly')

        time.sleep(5)
    except:
        continue
