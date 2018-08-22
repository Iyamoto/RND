"""
Having fun with stocks
"""

from stocker import Stocker
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from pprint import pprint

# st = Stocker(ticker='T')

# microsoft.plot_stock(start_date='2017-01-01')

# microsoft.buy_and_hold(start_date='2018-01-01', end_date='2018-05-05', nshares=10)

# model, model_data = st.create_prophet_model()
#
# model.plot_components(model_data)
# plt.show()

# microsoft.changepoint_date_analysis()

# model, future = st.create_prophet_model(days=180)

key = 'key'
symbol = 'INTC'

# Time Series
# ts = TimeSeries(key=key, output_format='pandas')
#
# data, meta_data = ts.get_daily_adjusted(symbol=symbol, outputsize='compact')
# data['4. close'].plot()
# plt.show()

# Technical indicators
ti = TechIndicators(key=key, output_format='pandas')

# RSI
# data, meta_data = ti.get_rsi(symbol=symbol, time_period=14, series_type='low')  # RSI 5
# print(data.tail(10).to_dict())

# MACD
data, meta_data = ti.get_macd(symbol=symbol, interval='daily', series_type='low')  # RSI 5
pprint(data.tail(10).to_dict())

# data.tail(10).plot()
# plt.show()
