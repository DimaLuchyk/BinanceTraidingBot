import DataObserver
import pandas as pd
from abc import ABC, abstractmethod
import TradeData
import logging

logger = logging.getLogger(__name__)

class TradeStrategyStep(ABC):
    @abstractmethod
    def process(self, data: TradeData.TradeData) -> None:
        pass


class TradeStrategy(DataObserver.DataObserver):
    def __init__(self, data: TradeData.TradeData):
        self.data = data
        self.steps: list[TradeStrategyStep] = []

    def update(self, data: pd.DataFrame) -> None:
        logger.debug("update method call start")
        if len(data) == 1:
            self.data.addCandle(data)
        else:
            self.data.addCandles(data)
        self.process(self.data)

        logger.debug("update method call end")

    def addStep(self, step: TradeStrategyStep):
        logger.debug("addStep method call start")

        print("addStep")
        self.steps.append(step)

        logger.debug("addStep method call end")

    def process(self, data: TradeData.TradeData) -> None:
        logger.debug("process method call start")

        for step in self.steps:
            step.process(data)
        
        logger.debug("process method call end")