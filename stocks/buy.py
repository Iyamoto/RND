"""
Stocks advisor
"""

import time
import alphaconf
import stockslib

key = alphaconf.key
timeout = 4

"""
"2018-08-23 10:50:34": {
"RSI": "54.3286"
},
"2018-08-22": {
"RSI": "48.3238"
},
"""

for symbol in alphaconf.symbols:
    print('====')
    print(symbol)

    prices = stockslib.get_prices(symbol=symbol, key=key)
    lastprices = stockslib.get_last_prices(pricedata=prices, type='close', points=1)
    sma20 = stockslib.get_sma(pricedata=prices, type='close', period=20, points=1)
    print('Last', lastprices)
    print('SMA20', sma20)

    buy = 0
    buy += stockslib.check_rsi(prices=prices, period=5)
    buy += stockslib.check_rsi(prices=prices, period=14)

    print('Buy advice', buy)

    sell = 0
    sell += stockslib.check_rsi_sell(prices=prices, period=5)
    sell += stockslib.check_rsi_sell(prices=prices, period=14)

    print('Sell advice', sell)

    # time.sleep(timeout)

    # Check MACD
    # stockslib.check_macd(symbol=symbol, key=alphaconf.key)
    # check_macd(symbol=symbol, key=alphaconf.key, interval='weekly')

    time.sleep(timeout)

    # exit()
