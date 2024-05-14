import pandas as pd
import websocket
import json
import SubjectOfInterest
import DataObserver
import TradeStrategy as ts

class LiveDataDownloader(SubjectOfInterest.SubjectOfInterest):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.ws = websocket.WebSocketApp(endpoint, on_open=self.__onOpen__, on_message=self.__onMessage__, on_close=self.__onClose__)
        tradeStrategy = ts.TradeStrategy()
        self.attach(tradeStrategy)


    def __onOpen__(self, ws):
        print("WebSocket connection opened.")
        ws.send(json.dumps({"method": "SUBSCRIBE", "params": ["btcusdt@kline_1m"], "id": 1}))

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
            self.notify(pd.json_normalize(kandle))
    
    def notify(self, data: pd.DataFrame) -> None:
        for sub in self.subsribers:
            sub.update(data)
    
    def attach(self, observer: DataObserver) -> None:
        self.subsribers.append(observer)
        pass

    def detach(self, observer: DataObserver) -> None:
        self.subsribers.remove(observer)
        pass

    def start(self):
        self.ws.run_forever()
    
    subsribers: list[DataObserver.DataObserver] = []