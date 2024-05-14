import pandas as pd
from enum import Enum

max_lines = 500

class TradeData:
    class TradeState(Enum):
        UNKNOWN = -1
        SET_SUP_RES = 0
        LOCATE_BREAK = 1
        #PRICE_IS_NEAR_NEW_SUP_OR_RES
        #PRICE_MOVES_IN_RIGHT_DIRECTION
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.tail(max_lines)
        self.state = TradeData.TradeState(TradeData.TradeState.UNKNOWN)
    
    def getState(self) -> TradeState:
        return self.state
    
    def setState(self, state: TradeState) -> None:
        self.state = state

    def addKandle(self, kandle: pd.DataFrame) -> None:
        self.data = pd.concat([self.data, kandle], ignore_index=True).tail(max_lines)