"""
Checks for good buy options
"""

import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time
import alphaconf
import stockslib

key = alphaconf.key
timeout = 5

for symbol in alphaconf.symbols:
    print('====')
    print(symbol)

    prices = stockslib.get_prices(symbol=symbol, key=key)
    lastprices = stockslib.get_last_prices(pricedata=prices, type='close', points=1)
    sma20 = stockslib.get_sma(pricedata=prices, type='close', period=20, points=1)
    rsi14 = stockslib.get_rsi(pricedata=prices, type='close', period=14, points=1)
    print(lastprices)
    print(sma20)
    print(rsi14)

    exit()

    try:

        prices = stockslib.get_prices(symbol=symbol, key=key)
        lastprices = stockslib.get_last_prices(pricedata=prices, type='close', points=1)
        sma20 = stockslib.get_sma(pricedata=prices, type='close', period=20, points=1)
        rsi14 = stockslib.get_rsi(pricedata=prices, type='close', period=14, points=1)
        print(lastprices)
        print(sma20)
        print(rsi14)

        # Check RSI
        # stockslib.check_rsi(symbol=symbol, key=alphaconf.key, time=5)
        # check_rsi(symbol=symbol, key=alphaconf.key, time=14)

        # time.sleep(timeout)

        # Check MACD
        # stockslib.check_macd(symbol=symbol, key=alphaconf.key)
        # check_macd(symbol=symbol, key=alphaconf.key, interval='weekly')

        time.sleep(timeout)
    except:
        print('Something failed')
        exit()
        continue

    exit()
