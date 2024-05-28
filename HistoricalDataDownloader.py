import pandas as pd
import logging
import SubjectOfInterest
import DataObserver

logger = logging.getLogger(__name__)

class HistoricalDataDownloader(SubjectOfInterest.SubjectOfInterest):
    def __init__(self, client, dataObserver: DataObserver.DataObserver):
        self.client = client
        self.subscribe(dataObserver)
    
    def getBinanceHistoricalData(self, symbol, interval, startStr):
        logger.debug("getBinanceHistoricalData method call start")
        logger.info("getBinanceHistoricalData. symbol: {}, interval: {}, startStr{}".format(symbol, interval, startStr))
        klines = self.client.get_historical_klines(symbol, interval, startStr)

        # Convert data to DataFrame
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        # Exclude the last row (the most recent kline)
        df = df[:-1]
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        #df.set_index('timestamp', inplace=True)
        selected_columns = ['timestamp', 'open', 'high', 'low', 'close', 'close_time']
        df_selected = df[selected_columns]
        df_selected['open'] = df_selected['open'].astype(float)
        df_selected['high'] = df_selected['high'].astype(float)
        df_selected['low'] = df_selected['low'].astype(float)
        df_selected['close'] = df_selected['close'].astype(float)

        self.notify(df_selected)

        logger.debug("getBinanceHistoricalData method call start")

        return df_selected
    
    def notify(self, data: pd.DataFrame) -> None:
        logger.debug("notify method call start")
        for sub in self.subsribers:
            sub.update(data)
        logger.debug("notify method call end")
    
    def subscribe(self, observer: DataObserver) -> None:
        self.subsribers.append(observer)
        pass

    def unsubscribe(self, observer: DataObserver) -> None:
        self.subsribers.remove(observer)
        pass

    subsribers: list[DataObserver.DataObserver] = []