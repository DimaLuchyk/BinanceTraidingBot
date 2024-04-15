from binance.client import Client
import datetime as dt
import pandas as pd

#real
#api_key = "HCjELFxQ0A49VqkckjWsZ8OoyKQDmLRWnybC0Jv6seUhdGCJglSNWNG90021jc3n"
#api_secret = "gzbVrIp01e8gHRqgu4RICUrknZUWm9J6TBdeNDitpX4LJ00Z4gArF3PgxQZ73ujl"

#testnet
api_key = "9f284aad3af2daa858ea0cf471f5e3ff4d864bde21927a33fb38fe914e57269a"
api_secret = "3244b9a49d5cbdd8918d9a2a041ff472e0a793941d40ca75684851a0badee35d"

client = Client(api_key,  api_secret)

symbol = "BTCUSDT"
interval = "15m"
start_time = dt.datetime.now() - dt.timedelta(hours=24)
end_time = dt.datetime.now()

print(start_time)
print(end_time)

# get the kline data from Binance server
klines = client.futures_historical_klines(symbol, 
                                          interval, 
                                          str(start_time), 
                                          str(end_time))

# convert the json data to pd.DataFrame 
klines_data = pd.DataFrame(klines)
klines_data.columns = ['open_time',
                       'open', 
                       'high', 
                       'low', 
                       'close', 
                       'volume',
                       'close_time',
                       'qav',
                       'num_trades',
                       'taker_base_vol',
                       'taker_quote_vol',
                       'ignore']

# convert data to appropriate data types
klines_data['close_time'] = [dt.datetime.fromtimestamp(x/1000.0) for x in klines_data["close_time"]]
klines_data['open_time'] = [dt.datetime.fromtimestamp(x/1000.0) for x in klines_data["open_time"]]
klines_data['close'] = klines_data['close'].astype('float')
klines_data['open'] = klines_data['open'].astype('float')
klines_data['high'] = klines_data['high'].astype('float')
klines_data['low'] = klines_data['low'].astype('float')

print(klines_data.to_string(index=False))

client.futures_create_order(symbol=symbol, 
                            side='BUY', 
                            type='MARKET', 
                            quantity=10)