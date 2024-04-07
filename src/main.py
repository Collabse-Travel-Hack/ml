from fastapi import FastAPI

from src.config.settings import ELASTICSEARCH_HOST
from src.api.endpoints import router
from src.data.preprocess_storage.elastic_search_storage import ElasticSearchStorage
from src.data.preprocessing.place_preprocessor import PlacePreprocessor
from src.data.database.mongo_database import MongoDatabase


def migrate_data():
    mongo_db = MongoDatabase(db_name='storage', collection_name='all_objects')
    mongo_db.connect()

    elastic = ElasticSearchStorage(host=ELASTICSEARCH_HOST)

    preprocessor = PlacePreprocessor(storage=elastic)
    data = mongo_db.find({})
    preprocessor.preprocess(data)

    mongo_db.disconnect()


app = FastAPI()

app.include_router(router)

# def main():
#     # migrate_data()
#
#     get_text_embeddings_params()
#
#     # elasric = ElasticDatabase(host=ELASTICSEARCH_HOST)
#     # elasric.connect()
#
#     # storage = WeaviateStorage()
#     # storage.delete_index()
#
#
# if __name__ == '__main__':
#     main()
