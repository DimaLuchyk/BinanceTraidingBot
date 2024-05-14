import HistoricalDataDownloader as hdd
import LiveDataDownloader as ldd
from binance.client import Client
import datetime as dt
import pandas as pd
import SubjectOfInterest
import DataObserver

api_key = 'HCjELFxQ0A49VqkckjWsZ8OoyKQDmLRWnybC0Jv6seUhdGCJglSNWNG90021jc3n'
api_secret = 'gzbVrIp01e8gHRqgu4RICUrknZUWm9J6TBdeNDitpX4LJ00Z4gArF3PgxQZ73ujl'
symbol = "BTCUSDT"
interval = "1m"

startTime = (dt.datetime.now(dt.UTC) - dt.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

endpoint = "wss://stream.binance.com:443/ws"

class BinanceDataReceiver:
    def __init__(self):
        client = Client(api_key, api_secret)

        self.historicalDataDownloader = hdd.HistoricalDataDownloader(client)
        self.liveDataDownloader = ldd.LiveDataDownloader(endpoint)
    
    def start(self):
        historicalData = self.historicalDataDownloader.getBinanceHistoricalData(symbol, interval, startTime)
        print(historicalData)
        self.liveDataDownloader.start()