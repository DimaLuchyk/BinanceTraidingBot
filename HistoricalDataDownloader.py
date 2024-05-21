import pandas as pd
import logging
import SubjectOfInterest
import DataObserver

logger = logging.getLogger(__name__)

api_key = 'HCjELFxQ0A49VqkckjWsZ8OoyKQDmLRWnybC0Jv6seUhdGCJglSNWNG90021jc3n'
api_secret = 'gzbVrIp01e8gHRqgu4RICUrknZUWm9J6TBdeNDitpX4LJ00Z4gArF3PgxQZ73ujl'

class HistoricalDataDownloader(SubjectOfInterest.SubjectOfInterest):
    def __init__(self, client, dataObserver: DataObserver.DataObserver):
        self.client = client
        self.subscribe(dataObserver)
    
    def getBinanceHistoricalData(self, symbol, interval, startStr):
        logger.debug("getBinanceHistoricalData method call start")

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
        # Specify the file path where you want to write the DataFrame
        file_path = 'output.csv'

        # Write the DataFrame to a CSV file
        df_selected.to_csv(file_path, index=False)

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