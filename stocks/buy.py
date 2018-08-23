"""
Stocks advisor
"""

import alphaconf
import stockslib

key = alphaconf.key

tobuy = dict()
tosell = dict()

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
    buy += stockslib.check_ema5_above_ema20(prices=prices)
    buy += stockslib.check_ema20_above_ema50(prices=prices)
    buy += stockslib.check_sma20_above_sma100(prices=prices)

    buy += stockslib.check_macd(prices=prices)

    print('Buy advice', buy)

    if buy > 6:
        tobuy[symbol] = [buy, lastprice]

    if lastprice > price > 0 and (price/lastprice - 1)*100 > 5:
        sell = 0
        sell += stockslib.check_rsi_sell(prices=prices, period=5)
        sell += stockslib.check_rsi_sell(prices=prices, period=14)

        print('Sell advice', sell)
        income = (price / lastprice) * 100
        print('Income', income)

        if sell > 5:
            tosell[symbol] = [sell, income]

print()
print('====================')
print('BUY:')
print(tobuy)
print('SELL:')
print(tosell)
