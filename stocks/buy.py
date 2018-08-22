"""
Checks for good buy options
"""

import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from pprint import pprint
import alphaconf

key = alphaconf.key
symbol = 'INTC'


def check_rsi(symbol='', key='', time=5, treshold=35, points=10):
    ti = TechIndicators(key=key, output_format='pandas')
    data, meta_data = ti.get_rsi(symbol=symbol, time_period=time, series_type='low')
    rsidata = data.tail(points).to_dict()
    for rsi in rsidata['RSI']:
        if rsidata['RSI'][rsi] < treshold:
            print(rsi, rsidata['RSI'][rsi])


def check_macd(symbol='', key='', interval='daily', points=10):
    """
    https://mindspace.ru/abcinvest/shozhdenie-rashozhdenie-skolzyashhih-srednih-moving-average-convergence-divergence-macd/
    https://mindspace.ru/abcinvest/aleksandr-elder-o-rashozhdeniyah-tseny-i-macd/
    https://mindspace.ru/30305-kak-ispolzovat-divergentsii-macd-dlya-vyyavleniya-razvorota-na-rynke/
    """
    ti = TechIndicators(key=key, output_format='pandas')
    data, meta_data = ti.get_macd(symbol=symbol, interval=interval, series_type='low')
    macddata = data.tail(points).to_dict()
    last = None
    for macd_date in macddata['MACD_Hist']:
        macd_value = macddata['MACD_Hist'][macd_date]
        if not last:
            last = macd_value
            continue

        if last < 0 and macd_value > 0:
            print(macd_date, last, macd_value)

        last = macd_value


# Lets start
print(symbol)

# Check RSI
print('Check if RSI(5) or RSI(14) are below 35')
print('RSI 5')
check_rsi(symbol=symbol, key=alphaconf.key, time=5)
print('RSI 14')
check_rsi(symbol=symbol, key=alphaconf.key, time=14)

# Check MACD
print('MACD moves over MACD signal line')
print('MACD daily')
check_macd(symbol=symbol, key=alphaconf.key)
print('MACD weekly')
check_macd(symbol=symbol, key=alphaconf.key, interval='weekly')

# data.tail(10).plot()
# plt.show()
