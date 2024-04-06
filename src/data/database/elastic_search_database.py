from elasticsearch import Elasticsearch

from src.data.database.base import DatabaseABC


class ElasticDatabase(DatabaseABC):
    def __init__(self, host):
        self.client = None
        self.host = host

    def connect(self, **kwargs):
        self.client = Elasticsearch(self.host, **kwargs)

    def disconnect(self):
        if self.client:
            self.client.close()

    def insert(self, index, data):
        result = self.client.index(index=index, body=data)
        return result['_id']

    def find(self, index, query):
        result = self.client.search(index=index, body=query)
        return [hit['_source'] for hit in result['hits']['hits']]

    def get_all(self, index):
        scroll_time = '5m'
        page_size = 1000

        # Инициализация поиска с прокруткой
        result = self.client.search(
            index=index,
            body={
                'query': {
                    'match_all': {}
                }
            },
            scroll=scroll_time,
            size=page_size
        )

        scroll_id = result['_scroll_id']
        hits = result['hits']['hits']

        # Итерация по страницам результатов
        while len(hits) > 0:
            # Обработка текущей страницы результатов
            for hit in hits:
                yield hit['_source']

            # Получение следующей страницы результатов
            result = self.client.scroll(scroll_id=scroll_id, scroll=scroll_time)
            scroll_id = result['_scroll_id']
            hits = result['hits']['hits']
