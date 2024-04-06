from abc import ABC, abstractmethod


class PreprocessorABC(ABC):
    @abstractmethod
    def preprocess(self, data):
        pass
