from fastapi import FastAPI

from config.settings import ELASTICSEARCH_HOST
from src.api.endpoints import router
from src.data.database.elastic_search_database import ElasticDatabase
from src.data.preprocess_storage.elastic_search_storage import ElasticSearchStorage
from src.data.preprocess_storage.weaviate_storage import WeaviateStorage
from src.data.preprocessing.place_preprocessor import PlacePreprocessor
from src.data.preprocessing.text_embeddings_preprocessor import TextEmbeddingsPreprocessor
from src.data.utils.embedder import RuBERTEmbedder
from src.data.database.mongo_database import MongoDatabase


def migrate_data():
    mongo_db = MongoDatabase(db_name='storage', collection_name='all_objects')
    mongo_db.connect()

    elastic = ElasticSearchStorage(host=ELASTICSEARCH_HOST)

    preprocessor = PlacePreprocessor(storage=elastic)
    data = mongo_db.find({})
    preprocessor.preprocess(data)

    mongo_db.disconnect()

def get_text_embeddings_params():
    elasric = ElasticDatabase(host=ELASTICSEARCH_HOST)
    elasric.connect()
    storage = WeaviateStorage()
    # storage.create_index()
    embedder = RuBERTEmbedder()
    data = elasric.get_all(index='places')
    text_embeddings_preprocessor = TextEmbeddingsPreprocessor(storage=storage, embedder=embedder, batch_size=32)
    text_embeddings_preprocessor.preprocess(data)
    elasric.disconnect()

app = FastAPI()

app.include_router(router)

# def main():
#     # migrate_data()
#
#     # get_text_embeddings_params()
#
#     app = FastAPI()
#
#     app.include_router(router)
#
#     # elasric = ElasticDatabase(host=ELASTICSEARCH_HOST)
#     # elasric.connect()
#     #
#     # for item in elasric.get_all(index='places'):
#     #     print(item)
#     #
#     # elasric.disconnect()
#
#
# if __name__ == '__main__':
#     main()
