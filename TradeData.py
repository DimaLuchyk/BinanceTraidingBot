import pandas as pd
from enum import Enum
import logging
import TrendLine

logger = logging.getLogger(__name__)

max_lines = 500

class TradeData:
    def __init__(self):
        self.data = pd.DataFrame()
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
        self.data = pd.concat([self.data, candle], ignore_index=True).tail(max_lines)
        print("data after adding candle: {}".format(self.data))
        logger.debug("addCandle method call end")

    def getLength(self) -> int:
        return len(self.data)
    
    def getRawData(self) -> pd.DataFrame:
        return self.data