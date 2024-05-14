from abc import ABC, abstractmethod
import pandas as pd

class DataObserver(ABC):
    @abstractmethod
    def update(self, data: pd.DataFrame) -> None:
        pass