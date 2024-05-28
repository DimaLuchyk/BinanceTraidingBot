import pandas as pd
from enum import Enum
import logging
import TrendLine

logger = logging.getLogger(__name__)

max_lines = 500

class TradeData:
    def __init__(self):
        self.data = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'close_time', 'isPivot', 'trueRange', 'pattern_detected', 'againInLevelZone', 'openTransaction', 'openedTransaction'])
        self.resistanceTrendLine = TrendLine.TrendLine()
        self.supportTrendLine = TrendLine.TrendLine()

    def setResistanceLine(self, values, trendLineHalfZone):
        self.resistanceTrendLine.setTrendLineValues(TrendLine.TrendLineType.RESITANCE, values, trendLineHalfZone)
    
    def setSupportLine(self, values, trendLineHalfZone):
        self.supportTrendLine.setTrendLineValues(TrendLine.TrendLineType.SUPPORT, values, trendLineHalfZone)
    
    def getResistanceTrendLine(self):
        return self.resistanceTrendLine
    
    def getSupportTrendLine(self):
        return self.supportTrendLine

    def addCandle(self, candle: pd.DataFrame) -> None:
        logger.debug("addCandle method call start")
        print("new_candle: {}".format(candle))
        #self.data = pd.concat([self.data, candle], ignore_index=True).tail(max_lines)

        new_row = {'timestamp': candle.loc[0].timestamp, 'open': candle.loc[0].open, 'high': candle.loc[0].high, 'low': candle.loc[0].low, 'close': candle.loc[0].close, 'close_time': candle.loc[0].close_time, 'isPivot': 0, 'trueRange': 0, 'pattern_detected': 0, 'againInLevelZone': 0, 'openTransaction': 0, 'openedTransaction': 0}
        self.data.loc[len(self.data)] = new_row
        self.data = self.data.tail(max_lines)
        print("data after adding candle: {}".format(self.data))
        logger.debug("addCandle method call end")

    def addCandles(self, candles: pd.DataFrame) -> None:
        logger.debug("addCandles method call start")
        self.data = pd.concat([self.data, candles], ignore_index=True).tail(max_lines)
        logger.debug("addCandles method call start")
        

    def getLength(self) -> int:
        return len(self.data)
    
    def getRawData(self) -> pd.DataFrame:
        return self.data