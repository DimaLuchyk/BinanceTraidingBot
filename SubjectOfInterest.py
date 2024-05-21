from abc import ABC, abstractmethod
from DataObserver import DataObserver
import pandas as pd

class SubjectOfInterest(ABC):
    @abstractmethod
    def subscribe(self, observer: DataObserver) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, observer: DataObserver) -> None:
        pass

    @abstractmethod
    def notify(self, data: pd.DataFrame) -> None:
        pass