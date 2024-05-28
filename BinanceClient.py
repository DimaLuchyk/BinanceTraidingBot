from binance.client import Client
from binance.enums import *
import math
import ConfigurationReader
import logging

logger = logging.getLogger(__name__)

class BinanceClient:
    def __init__(self, api_key, api_secret, testnet=False):
        self.client = Client(api_key, api_secret, testnet=testnet)

    def get_current_price(self, symbol):
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            return f"An error occurred: {e}"
    
    def usdtToQuantity(self, usdtValue, currentPrice):
        return round(usdtValue / currentPrice, 3)

    def openLongPositionMarket(self, symbol, usdtQuantity):
        try:
            currentPrice = self.get_current_price(symbol)
            if isinstance(currentPrice, str):
                logger.error("failed to receive current price of {}, error message: {}".format(symbol, currentPrice))
                print("failed to receive current price of {}, error message: {}".format(symbol, currentPrice))
            quantity = self.usdtToQuantity(usdtQuantity, currentPrice)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return order
        except Exception as e:
            return f"An error occurred: {e}"
    
    def openShortPositionMarket(self, symbol, usdtQuantity):
        try:
            currentPrice = self.get_current_price(symbol)
            if isinstance(currentPrice, str):
                logger.error("failed to receive current price of {}, error message: {}".format(symbol, currentPrice))
                print("failed to receive current price of {}, error message: {}".format(symbol, currentPrice))
            quantity = self.usdtToQuantity(usdtQuantity, currentPrice)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return order
        except Exception as e:
            return f"An error occurred: {e}"

    def close_position_market(self, symbol):
        try:
            position_info = self.get_position_info(symbol)
            if position_info:
                position_amt = float(position_info['positionAmt'])
                side = "SELL" if position_amt > 0 else "BUY"  # Opposite side to close the position
                quantity = abs(position_amt)

                # Place a market order to close the position
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
                return order
            else:
                return "No open position to close."
        except Exception as e:
            return f"An error occurred: {e}"

    def calculateLeverage(self, currentValue: int, stopLossValue: int):
        stopLossCount = abs(currentValue - stopLossValue)
        stopLossPercent = stopLossCount/(currentValue*0.01)
        leverage = 20 / stopLossPercent
        return math.floor(leverage)
    
    def calculateTakeProfitForLong(self, currentValue: int, stopLossValue: int):
        stopLossCount = abs(currentValue - stopLossValue)
        longTakeProfitValue = currentValue + (3*stopLossCount)
        return math.floor(longTakeProfitValue)

    def calculateTakeProfitForShort(self, currentValue: int, stopLossValue: int):
        stopLossCount = abs(currentValue - stopLossValue)
        shortTakeProfitValue = currentValue - (3*stopLossCount)
        return math.floor(shortTakeProfitValue)

    def open_long_and_set_sp_tp(self, symbol, quantity, stop_loss_price, take_profit_price):
        try:
            # Open long position
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=quantity
            )

            # Set stop loss and take profit
            stop_loss_order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=FUTURE_ORDER_TYPE_STOP_MARKET,
                quantity=abs(quantity),
                stopPrice=stop_loss_price
            )
            take_profit_order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,
                quantity=abs(quantity),
                stopPrice=take_profit_price
            )
            return order, stop_loss_order, take_profit_order
        except Exception as e:
            return f"An error occurred: {e}"

    def open_short_and_set_sp_tp(self, symbol, quantity, stop_loss_price, take_profit_price):
        try:
            # Open short position
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=quantity
            )

            # Set stop loss and take profit
            stop_loss_order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=FUTURE_ORDER_TYPE_STOP_MARKET,
                quantity=abs(quantity),
                stopPrice=stop_loss_price
            )
            take_profit_order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,
                quantity=abs(quantity),
                stopPrice=take_profit_price
            )
            return order, stop_loss_order, take_profit_order
        except Exception as e:
            return f"An error occurred: {e}"

    def openLong(self, symbol: str, usdtQuantity: int, currentValue: int, stopLossValue: int):
        currentPrice = self.get_current_price(symbol)
        if isinstance(currentPrice, str):
            print("failed to receive current price of {}, error message: {}".format(symbol, currentPrice))
        quantity = self.usdtToQuantity(usdtQuantity, currentPrice)
        leverage = self.calculateLeverage(currentValue, stopLossValue)
        self.set_leverage(symbol, leverage)
        takeProfitValue = self.calculateTakeProfitForLong(currentValue, stopLossValue)
        logger.info("open LONG, symbol: {}, quantity: {}, stopLossValue: {}, takeProfitValue: {}".format(symbol, quantity, stopLossValue, takeProfitValue))
        print("open LONG, symbol: {}, quantity: {}, stopLossValue: {}, takeProfitValue: {}".format(symbol, quantity, stopLossValue, takeProfitValue))
        return self.open_long_and_set_sp_tp(symbol, quantity * leverage, stopLossValue, takeProfitValue)
    
    def openShort(self, symbol: str, usdtQuantity: int, currentValue: int, stopLossValue: int):
        currentPrice = self.get_current_price(symbol)
        if isinstance(currentPrice, str):
            print("failed to receive current price of {}, error message: {}".format(symbol, currentPrice))
        quantity = self.usdtToQuantity(usdtQuantity, currentPrice)
        leverage = self.calculateLeverage(currentValue, stopLossValue)
        self.set_leverage(symbol, leverage)
        takeProfitValue = self.calculateTakeProfitForShort(currentValue, stopLossValue)
        logger.info("open SHORT, symbol: {}, quantity: {}, stopLossValue: {}, takeProfitValue: {}".format(symbol, quantity, stopLossValue, takeProfitValue))
        print("open SHORT, symbol: {}, quantity: {}, stopLossValue: {}, takeProfitValue: {}".format(symbol, quantity, stopLossValue, takeProfitValue))
        return self.open_short_and_set_sp_tp(symbol, quantity * leverage, stopLossValue, takeProfitValue)

    def set_leverage(self, symbol, leverage):
        try:
            leverage_response = self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            return leverage_response
        except Exception as e:
            return f"An error occurred: {e}"

    def get_position_info(self, symbol):
        try:
            positions = self.client.futures_position_information(symbol=symbol)
            for position in positions:
                if float(position['positionAmt']) != 0:  # Check if there is an open position
                    return position
            return None
        except Exception as e:
            return f"An error occurred: {e}"

    def get_account_balance(self):
        try:
            balance_info = self.client.futures_account_balance()
            return balance_info
        except Exception as e:
            return f"An error occurred: {e}"

#client = BinanceClient(api_key=api_key, api_secret=api_secret, testnet=True)
#client.set_leverage(symbol, 20)
#print(client.get_account_balance())
#client.openLongPositionMarket(symbol, 0.1)
#client.close_position_market(symbol)
#client.open_long_and_set_sp_tp(symbol, 0.1, 65000,67000)
#print(client.open_short_and_set_sp_tp(symbol, 0.1, 68000, 62000))
#print(client.openLong(symbol, 500, client.get_current_price(symbol), client.get_current_price("BTCUSDT") - 500))