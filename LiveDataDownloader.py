import pandas as pd
import websocket
import json
import SubjectOfInterest
import DataObserver
import TradeStrategy as ts
import TradeData
import logging
import ConfigurationReader

logger = logging.getLogger(__name__)

class LiveDataDownloader(SubjectOfInterest.SubjectOfInterest):
    def __init__(self, endpoint: str, dataObserver: DataObserver.DataObserver):
        self.endpoint = endpoint
        self.ws = websocket.WebSocketApp(endpoint, on_open=self.__onOpen__, on_message=self.__onMessage__, on_close=self.__onClose__)
        self.subscribe(dataObserver)


    def __onOpen__(self, ws):
        print("WebSocket connection opened.")
        symbol = ConfigurationReader.get("symbol")
        interval = ConfigurationReader.get("interval")
        symbolLower = symbol.lower()
        params_string = f"{symbolLower}@kline_{interval}"

        logger.info(f"about to send subscribe method to the websocket with the following params_string:{params_string}")

        ws.send(json.dumps({"method": "SUBSCRIBE", "params": [params_string], "id": 1}))

    def __onClose__(self, ws):
        print("WebSocket connection closed.")

    def __onMessage__(self, ws, message):
        json_message = json.loads(message)
        kandle = json_message['k']
        kandle_closed = kandle['x']
        kandle['t'] = pd.to_datetime(kandle['t'], unit='ms')
        kandle['T'] = pd.to_datetime(kandle['T'], unit='ms')
        open_data = kandle['o']
        close_data = kandle['c']
        low_data = kandle['l']
        high_data = kandle['h']
        is_closed = 1 if kandle_closed else 0
        if is_closed:
            logger.debug("new candle, notify subs")
            dfCandle = pd.json_normalize(kandle)
            dfCandleSelected = dfCandle[['t', 'o', 'h', 'l', 'c', 'T']]
            new_names = {
                't': 'timestamp',
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
                'T': 'close_time'
            }
            dfCandleSelected = dfCandleSelected.rename(columns=new_names)
            # Add new columns with value 0
            new_columns = ['isPivot', 'trueRange', 'pattern_detected', 'againInLevelZone', 'openTransaction', 'openedTransaction']
            for column in new_columns:
                dfCandleSelected[column] = 0
            dfCandleSelected = dfCandleSelected.round(2)
            self.notify(dfCandleSelected)
    
    def notify(self, data: pd.DataFrame) -> None:
        logger.debug("notify method call start")

        if data.empty:
            print("notify, received empty data")
        else:
            print("notify, received not empty data")

        for sub in self.subsribers:
            sub.update(data)
        logger.debug("notify method call end")
    
    def subscribe(self, observer: DataObserver) -> None:
        self.subsribers.append(observer)
        pass

    def unsubscribe(self, observer: DataObserver) -> None:
        self.subsribers.remove(observer)
        pass

    def start(self):
        logger.debug("start listening for data from websocket")
        self.ws.run_forever()
    
    subsribers: list[DataObserver.DataObserver] = []


