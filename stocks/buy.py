"""
Stocks advisor
"""

import alphaconf
import stockslib

key = alphaconf.key

for item in alphaconf.symbols:
    if type(item) == dict:
        price = list(item.values())[0]
        symbol = list(item.keys())[0]
    else:
        symbol = item
        price = 0

    print('====')
    print(symbol, price)

    prices = stockslib.get_prices(symbol=symbol, key=key)
    lastprice = stockslib.get_last_price(price=prices, type='close')

    buy = 0
    buy += stockslib.check_rsi(prices=prices, period=5)
    buy += stockslib.check_rsi(prices=prices, period=14)

    buy += stockslib.check_price_close_sma(prices=prices, period=20)
    buy += stockslib.check_price_close_sma(prices=prices, period=50)
    buy += stockslib.check_price_close_sma(prices=prices, period=200)

    buy += stockslib.check_price_above_ema(prices=prices, period=50)

    buy += stockslib.check_macd(prices=prices)

    print('Buy advice', buy)

    if lastprice > price > 0 and (price/lastprice - 1)*100 > 5:
        sell = 0
        sell += stockslib.check_rsi_sell(prices=prices, period=5)
        sell += stockslib.check_rsi_sell(prices=prices, period=14)

        print('Sell advice', sell)
        print('Income', (price / lastprice) * 100)
