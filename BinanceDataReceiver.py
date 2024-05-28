import HistoricalDataDownloader as hdd
import LiveDataDownloader as ldd
from binance.client import Client
import datetime as dt
import pandas as pd
import TradeStrategy as ts
import TradeData as td
import ConcreteTradeStrategySteps as steps
import ConfigurationReader
import logging

logger = logging.getLogger(__name__)

startTime = (dt.datetime.now(dt.UTC) - dt.timedelta(minutes=90)).strftime("%Y-%m-%d %H:%M:%S")

endpoint = "wss://stream.binancefuture.com:443/ws"

class BinanceDataReceiver:
    def __init__(self):
        api_key = ConfigurationReader.get("api_key")
        api_secret = ConfigurationReader.get("api_secret")
        testnet = ConfigurationReader.get("testnet")
        logger.info("about to start client for HistoricalDataDownloader with the following settings. api_key: {}, api_secret: {}, testnet: {}".format(api_key, api_secret, testnet))
        client = Client(api_key, api_secret, testnet=True)

        tradeData = td.TradeData()
        tradeStrategy = ts.TradeStrategy(tradeData)
        tradeStrategy.addStep(steps.ConcreteStep1())
        tradeStrategy.addStep(steps.ConcreteStep2())
        tradeStrategy.addStep(steps.ConcreteStep3())
        tradeStrategy.addStep(steps.ConcreteStep4())
        tradeStrategy.addStep(steps.ConcreteStep5())

        self.historicalDataDownloader = hdd.HistoricalDataDownloader(client, tradeStrategy)

        logger.info("endpoint for liveDataDownloader: {}".format(endpoint))

        self.liveDataDownloader = ldd.LiveDataDownloader(endpoint, tradeStrategy)
    
    def start(self):
        symbol = ConfigurationReader.get("symbol")
        interval = ConfigurationReader.get("interval")

        self.historicalDataDownloader.getBinanceHistoricalData(symbol, interval, startTime)
        self.liveDataDownloader.start()