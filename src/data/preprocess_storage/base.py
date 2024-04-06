from abc import ABC, abstractmethod


class StorageABC(ABC):
    @abstractmethod
    def save(self, data, path):
        pass

    @abstractmethod
    def load(self, path):
        pass

    @abstractmethod
    def search(self, path, query):
        pass
