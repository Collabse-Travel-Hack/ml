from abc import ABC, abstractmethod

class DatabaseABC(ABC):
    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def insert(self, index, data):
        pass

    @abstractmethod
    def find(self, index, query):
        pass

    @abstractmethod
    def get_all(self, index):
        pass