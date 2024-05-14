import pandas as pd

api_key = 'HCjELFxQ0A49VqkckjWsZ8OoyKQDmLRWnybC0Jv6seUhdGCJglSNWNG90021jc3n'
api_secret = 'gzbVrIp01e8gHRqgu4RICUrknZUWm9J6TBdeNDitpX4LJ00Z4gArF3PgxQZ73ujl'

class HistoricalDataDownloader:
    def __init__(self, client):
        self.client = client
    
    def getBinanceHistoricalData(self, symbol, interval, startStr):
        klines = self.client.get_historical_klines(symbol, interval, startStr)

        # Convert data to DataFrame
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        # Specify the file path where you want to write the DataFrame
        file_path = 'output.csv'

        # Write the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
        return df