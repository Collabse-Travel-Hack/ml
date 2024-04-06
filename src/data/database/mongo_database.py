from pymongo import MongoClient
from src.data.database.base import DatabaseABC
from src.config.settings import MONGODB_HOST


class MongoDatabase(DatabaseABC):
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self.host = MONGODB_HOST

    def connect(self, **kwargs):
        self.client = MongoClient(host=self.host, **kwargs)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def disconnect(self):
        self.client.close()

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, query):
        return self.collection.find(query)

    def get_all(self):
        pass
