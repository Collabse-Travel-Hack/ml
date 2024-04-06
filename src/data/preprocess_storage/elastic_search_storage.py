from elasticsearch import Elasticsearch
from data.preprocess_storage.base import StorageABC
from elasticsearch import helpers



class ElasticSearchStorage(StorageABC):
    def __init__(self, host):
        self.es = Elasticsearch(host)

    def create_index(self, path):
        if not self.es.indices.exists(index=path):
            mapping = {
                "mappings": {
                    "properties": {
                        "id": {"type": "keyword"},
                        "address": {"type": "text"},
                        "metro_station": {"type": "text"},
                        "object_type": {"type": "keyword"},
                        "popularity": {"type": "float"},
                        "title": {"type": "text"},
                        "description": {"type": "text"},
                        "has_audio_guide": {"type": "boolean"},
                        "is_can_buy": {"type": "boolean"},
                        "price": {"type": "float"},
                        "russpass_recommendation": {"type": "boolean"},
                        "rating": {"type": "float"},
                        "type": {"type": "keyword"}
                    }
                }
            }
            self.es.indices.create(index=path, body=mapping)

    def save(self, data, path):
        self.create_index(path)

        if isinstance(data, list):
            actions = [
                {
                    "_index": path,
                    "_source": {
                        "id": item.id,
                        "address": item.address,
                        "metro_station": item.metro_station,
                        "object_type": item.object_type.value,
                        "popularity": item.popularity,
                        "title": item.title,
                        "description": item.description,
                        "has_audio_guide": item.has_audio_guide,
                        "is_can_buy": item.is_can_buy,
                        "price": item.price,
                        "russpass_recommendation": item.russpass_recommendation,
                        "rating": item.rating,
                        "type": item.type
                    }
                }
                for item in data
            ]
            helpers.bulk(self.es, actions)
        else:
            self.es.index(index=path, body={
                "id": data.id,
                "address": data.address,
                "metro_station": data.metro_station,
                "object_type": data.object_type.value,
                "popularity": data.popularity,
                "title": data.title,
                "description": data.description,
                "has_audio_guide": data.has_audio_guide,
                "is_can_buy": data.is_can_buy,
                "price": data.price,
                "russpass_recommendation": data.russpass_recommendation,
                "rating": data.rating,
                "type": data.type
            })

    def load(self, path):
        pass

    def search(self, path, query):
        result = self.es.search(index=path, body={'query': {'match': {'_all': query}}})
        return [hit['_source'] for hit in result['hits']['hits']]