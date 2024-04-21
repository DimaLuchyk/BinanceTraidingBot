import mplfinance as mpf
from binance.client import Client
import datetime as dt
import pandas as pd
import numpy as np

# Binance API credentials
api_key = "HCjELFxQ0A49VqkckjWsZ8OoyKQDmLRWnybC0Jv6seUhdGCJglSNWNG90021jc3n"
api_secret = "gzbVrIp01e8gHRqgu4RICUrknZUWm9J6TBdeNDitpX4LJ00Z4gArF3PgxQZ73ujl"
client = Client(api_key, api_secret)

# Define symbol, interval, and time range
symbol = "BTCUSDT"
interval = "15m"
end_time = dt.datetime.now()
start_time = end_time - dt.timedelta(hours=24)

# Retrieve historical candlestick data
klines = client.futures_historical_klines(symbol, interval, start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S"))

# Convert data to DataFrame
columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]
df = pd.DataFrame(klines, columns=columns)

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Convert numeric columns to float
numeric_columns = ['open', 'high', 'low', 'close', 'volume']
df[numeric_columns] = df[numeric_columns].astype(float)

# Set datetime as index
df.set_index('timestamp', inplace=True)

supports = df[df['low'] == df['low'].rolling(5, center=True).min()]
resistances = df[df['high'] == df['high'].rolling(5, center=True).max()]

# Extracting support and resistance levels as lists
support_levels = supports['low'].tolist()
resistance_levels = resistances['high'].tolist()

average =  np.mean(df['high'] - df['low'])

# Combine support and resistance levels into a single list
levels = support_levels + resistance_levels

print("levels before filter: ", levels)

# Plot candlestick chart using mplfinance
#mpf.plot(df, type='candle', style='binance', title='BTCUSDT - 15m Candlestick', ylabel='Price (USDT)', volume=True, hlines=dict(hlines=levels))

s =  np.mean(df['high'] - df['low'])

def isFarFromLevel(l):
  return np.sum([abs(l-x) < s  for x in levels]) == 0

def isSupport(df,i):
  support = df['low'][i] < df['low'][i-1]  and df['low'][i] < df['low'][i+1] \
  and df['low'][i+1] < df['low'][i+2] and df['low'][i-1] < df['low'][i-2]

  return support

def isResistance(df,i):
  resistance = df['high'][i] > df['high'][i-1]  and df['high'][i] > df['high'][i+1] \
  and df['high'][i+1] > df['high'][i+2] and df['high'][i-1] > df['high'][i-2] 

  return resistance

levels = []
for i in range(2,df.shape[0]-2):
  if isSupport(df,i):
    l = df['low'][i]

    if isFarFromLevel(l):
      levels.append(l)

  elif isResistance(df,i):
    l = df['high'][i]

    if isFarFromLevel(l):
      levels.append(l)


print("after filter: ", levels)

mpf.plot(df, type='candle', style='binance', title='BTCUSDT - 15m Candlestick', ylabel='Price (USDT)', volume=True, hlines=dict(hlines=levels))