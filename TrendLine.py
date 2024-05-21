from enum import Enum

class TrendLineType(Enum):
        UNKNOWN = -1
        SUPPORT = 0
        RESITANCE = 1

class TrendLine:
    def __init__(self):
        self.type = TrendLineType.UNKNOWN
        self.values = []
        self.realTrendLineValue = 0
        self.trendLineHalfZone = 0
    
    def setTrendLineValues(self, type: TrendLineType, values: list, trendLineHalfZone: int):
        self.type = type
        self.values = values
        self.trendLineHalfZone = trendLineHalfZone
        self.realTrendLineValue = sum(values)/len(values)

    def isSupport(self):
        return self.type == TrendLineType.SUPPORT
    
    def isResistance(self):
        return self.type == TrendLineType.RESITANCE
    
    def getRealTrendLineValue(self):
        return self.realTrendLineValue

    def getTrendLineHalfZone(self):
        return self.trendLineHalfZone