from TradeStrategy import TradeStrategyStep
import TradeData
import pandas as pd
import BinanceClient
import ConfigurationReader


class ConcreteStep1(TradeStrategyStep):
    def process(self, data: TradeData.TradeData) -> None:
        df = data.getRawData()
        window = 5
        df['isPivot'] = df.apply(lambda x: self.__isPivot__(x.name, window, data), axis=1)
        df['trueRange'] = df.apply(lambda x: self.__calculateTrueRange__(x.name, data), axis=1)

    def __calculateTrueRange__(self, candle, data: TradeData.TradeData):
        df = data.getRawData()
    
        # Ensure 'high', 'low', and 'close' columns are numeric
        df['high'] = pd.to_numeric(df['high'], errors='coerce')
        df['low'] = pd.to_numeric(df['low'], errors='coerce')
        df['close'] = pd.to_numeric(df['close'], errors='coerce')

        if candle == 0:
            # If candle is 0, there's no previous close, handle this edge case
            return max(df.iloc[candle].high - df.iloc[candle].low, df.iloc[candle].high - df.iloc[candle].close, df.iloc[candle].low - df.iloc[candle].close)

        high_low = df.iloc[candle].high - df.iloc[candle].low  # Current high - current low
        high_close = abs(df.iloc[candle].high - df.iloc[candle - 1].close)  # Current high - previous close
        low_close = abs(df.iloc[candle].low - df.iloc[candle - 1].close)  # Current low - previous close

        # Calculate the True Range
        true_range = max(high_low, high_close, low_close)

        return true_range

    def __isPivot__(self, candle, window, data: TradeData.TradeData):
        if (candle - window < 0 or candle + window >= data.getLength()):
            return 0
        pivotHigh = 1
        pivotLow = 2

        df = data.getRawData()

        for i in range(candle - window, candle + window+1):
            if df.iloc[candle].low > df.iloc[i].low:
                pivotLow=0
            if df.iloc[candle].high < df.iloc[i].high:
                pivotHigh=0
    
        if pivotHigh and pivotLow:
            return 3
        elif pivotHigh:
            return pivotHigh
        elif pivotLow:
            return pivotLow
        else:
            return 0

class ConcreteStep2(TradeStrategyStep):
    def process(self, data: TradeData.TradeData) -> None:
        df = data.getRawData()
        df['pattern_detected'] = df.apply(lambda row: self.__detect_structure__(row.name, backcandles=80, window=4, data=data), axis=1)
    
    def __detect_structure__(self, candle, backcandles, window, data: TradeData.TradeData):
        if(candle <= (backcandles+window)) or (candle + window+1 >= data.getLength()):
            return 0
        
        df = data.getRawData()

        # Calculate the average range over the past ... periods
        atrWindow = 14
        atr = df['trueRange'].rolling(window=atrWindow).mean().iloc[candle]
        halfZone = atr

        print("halfZone: {}".format(halfZone))

        localdf = df.iloc[candle-backcandles-window:candle-window]
        highs = localdf[localdf['isPivot'] == 1].high.tail(2).values
        lows = localdf[localdf['isPivot'] == 2].low.tail(2).values

        levelbreak = 0
        if len(lows) == 2:
            support_condition = True
            mean_low = lows.mean()
            for low in lows:
                if abs(low-mean_low) > halfZone:
                    support_condition = False
                    break
                if support_condition and (mean_low - df.loc[candle].close) > halfZone:
                    levelbreak = 2
                
        if len(highs) == 2:
            resistance_condition = True
            mean_high = highs.mean()
            for high in highs:
                if abs(high - mean_high) > halfZone:
                    resistance_condition = False
                    break
                if resistance_condition and (df.loc[candle].close-mean_high) > halfZone:
                    levelbreak = 1
        
        if levelbreak == 1:
            data.setResistanceLine(highs.tolist(), halfZone)
            pass
        elif levelbreak == 2:
            data.setSupportLine(lows.tolist(), halfZone)
            pass

        return levelbreak 

class ConcreteStep3(TradeStrategyStep):
    def process(self, data: TradeData.TradeData) -> None:
        df = data.getRawData()
        df['againInLevelZone'] = df.apply(lambda row: self.__detectBackInZone__(row.name, data=data), axis=1)

    def __detectBackInZone__(self, candle, data: TradeData.TradeData):
        df = data.getRawData()

        breakResistanceLevelIndex = df[df['pattern_detected'] == 1].tail(1).index
        breakSupportLevelIndex = df[df['pattern_detected'] == 2].tail(1).index
        againInLevelZone = 0
        if candle <= breakResistanceLevelIndex or candle <= breakSupportLevelIndex:
            return againInLevelZone
        print("breakSUportLevelIndex: {}".format(breakSupportLevelIndex))
        print("breakResistanceLevelIndex: {}".format(breakResistanceLevelIndex))

        if breakResistanceLevelIndex > breakSupportLevelIndex:
            print("resistance was break")
            # get the resistance line that was break, now it's a potential support line
            potentialSupportLine = data.getResistanceTrendLine()

            if abs(potentialSupportLine.getRealTrendLineValue() - df.loc[candle].close) < potentialSupportLine.getTrendLineHalfZone():
                againInLevelZone = 2
        elif breakSupportLevelIndex > breakResistanceLevelIndex:
            print("support was break")
            # get the suport level that was break, not it's a potential resistance line
            potentialResistanceLine = data.getSupportTrendLine()

            if abs(df.loc[candle].close - potentialResistanceLine.getRealTrendLineValue()) < potentialResistanceLine.getTrendLineHalfZone():
                againInLevelZone = 1
        
        return againInLevelZone


class ConcreteStep4(TradeStrategyStep):
    def process(self, data: TradeData.TradeData) -> None:
        df = data.getRawData()
        df['openTransaction'] = df.apply(lambda row: self.__confirmNewSupportOrRessistanceLine__(row.name, data=data), axis=1)
        file_path = 'SUPRES.csv'

        # Write the DataFrame to a CSV file
        df.to_csv(file_path, index=False)

    def __confirmNewSupportOrRessistanceLine__(self, candle, data: TradeData.TradeData):
        df = data.getRawData()

        againInPotentialResistanceLevelIndex = df[df['againInLevelZone'] == 1].tail(1).index
        againInPotentialSupportLevelIndex = df[df['againInLevelZone'] == 2].tail(1).index
        
        openTransaction = 0
        if candle <= againInPotentialResistanceLevelIndex or candle <= againInPotentialSupportLevelIndex:
            return openTransaction
        
        print("againInPotentialResistanceLevelIndex: {}".format(againInPotentialResistanceLevelIndex))
        print("againInPotentialSupportLevelIndex: {}".format(againInPotentialSupportLevelIndex))

        openTransaction = 0
        if againInPotentialResistanceLevelIndex > againInPotentialSupportLevelIndex:
            print("againInPotentialResistanceLevelIndex")
            # get the suport level that was break, not it's a potential resistance level
            potentialResistanceTrendLine = data.getSupportTrendLine()
            diff = potentialResistanceTrendLine.getRealTrendLineValue() - df.loc[candle].close

            if diff > 0 and diff > potentialResistanceTrendLine.getTrendLineHalfZone():
                openTransaction = 1 #sell transaction
        elif againInPotentialSupportLevelIndex > againInPotentialResistanceLevelIndex:
            print("againInPotentialSupportLevelIndex")
            # get the resistance level that was break, not it's a potential support level
            potentialSupportTrendLine = data.getResistanceTrendLine()
            diff = df.loc[candle].close - potentialSupportTrendLine.getRealTrendLineValue()

            if diff > 0 and diff > potentialSupportTrendLine.getTrendLineHalfZone():
                openTransaction = 2 #buy transaction
        
        return openTransaction
    

class ConcreteStep5(TradeStrategyStep):
    def __init__(self):
        self.binanceClient = BinanceClient.BinanceClient(ConfigurationReader.get("api_key"), ConfigurationReader.get("api_secret"), testnet=ConfigurationReader.get("Testnet"))

    def process(self, data: TradeData.TradeData) -> None:
        df = data.getRawData()
        df['openedTransaction'] = df.apply(lambda row: self.__makeTransaction__(row.name, data=data), axis=1)
        file_path = 'SUPRES.csv'

        # Write the DataFrame to a CSV file
        df.to_csv(file_path, index=False)

    def __makeTransaction__(self, candle, data: TradeData.TradeData):
        df = data.getRawData()

        openTransactionShortIndex = df[df['openTransaction'] == 1].tail(1).index
        openTransactionLongIndex = df[df['openTransaction'] == 2].tail(1).index

        openedTransaction = 0
        if candle < openTransactionShortIndex or candle < openTransactionLongIndex:
            return openedTransaction

        print("openTransactionShortIndex: {}".format(openTransactionShortIndex))
        print("openTransactionLongIndex: {}".format(openTransactionLongIndex))

        if openTransactionLongIndex > openTransactionShortIndex:
            print("open long transaction")
            #get resistance trand line that was break, now it is confirmed support trend line
            supportTrendLine = data.getResistanceTrendLine()
            openedTransaction = 2
            print(self.binanceClient.openLong(ConfigurationReader.get("symbol"), 500, df.loc[candle].close, supportTrendLine.getRealTrendLineValue() - supportTrendLine.getTrendLineHalfZone()))

        elif openTransactionShortIndex > openTransactionLongIndex:
            print("open short transaction")
            #get support trand line that was break, now it is confirmed resistance trend line
            resistanceTrendLine = data.getSupportTrendLine()
            openedTransaction = 1
            print(self.binanceClient.openShort(ConfigurationReader.get("symbol"), 500, df.loc[candle].close, resistanceTrendLine.getRealTrendLineValue() + resistanceTrendLine.getTrendLineHalfZone()))
        
        return openedTransaction