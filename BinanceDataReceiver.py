import HistoricalDataDownloader as hdd
import LiveDataDownloader as ldd
from binance.client import Client
import datetime as dt
import pandas as pd
import TradeStrategy as ts
import TradeData as td
import ConcreteTradeStrategySteps as steps
import SubjectOfInterest
import DataObserver

api_key = 'HCjELFxQ0A49VqkckjWsZ8OoyKQDmLRWnybC0Jv6seUhdGCJglSNWNG90021jc3n'
api_secret = 'gzbVrIp01e8gHRqgu4RICUrknZUWm9J6TBdeNDitpX4LJ00Z4gArF3PgxQZ73ujl'
symbol = "BTCUSDT"
interval = "1m"

startTime = (dt.datetime.now(dt.UTC) - dt.timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")

endpoint = "wss://stream.binance.com:443/ws"

class BinanceDataReceiver:
    def __init__(self):
        client = Client(api_key, api_secret)

        tradeData = td.TradeData()
        tradeStrategy = ts.TradeStrategy(tradeData)
        tradeStrategy.addStep(steps.ConcreteStep1())
        tradeStrategy.addStep(steps.ConcreteStep2())
        tradeStrategy.addStep(steps.ConcreteStep3())

        self.historicalDataDownloader = hdd.HistoricalDataDownloader(client, tradeStrategy)
        self.liveDataDownloader = ldd.LiveDataDownloader(endpoint, tradeStrategy)
    
    def start(self):
        self.historicalDataDownloader.getBinanceHistoricalData(symbol, interval, startTime)
        self.liveDataDownloader.start()