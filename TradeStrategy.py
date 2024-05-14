import DataObserver
import pandas as pd

class TradeStrategy(DataObserver.DataObserver):
    def update(self, data: pd.DataFrame) -> None:
        print("[TradeStrategy] received new data: {}".format(data))
        pass