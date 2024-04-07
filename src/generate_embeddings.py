from src.data.utils.embedder import RuBERTEmbedder
from src.config.settings import ELASTICSEARCH_HOST, WEAVIATE_HOST
from src.data.database.elastic_search_database import ElasticDatabase
from src.data.preprocess_storage.weaviate_storage import WeaviateStorage
from src.data.preprocessing.text_embeddings_preprocessor import TextEmbeddingsPreprocessor


def get_text_embeddings_params():
    elasric = ElasticDatabase(host=ELASTICSEARCH_HOST)
    elasric.connect()
    storage = WeaviateStorage(host=WEAVIATE_HOST)
    storage.create_index()

    embedder = RuBERTEmbedder()

    data = elasric.get_all(index='places')
    text_embeddings_preprocessor = TextEmbeddingsPreprocessor(storage=storage, embedder=embedder, batch_size=32)
    text_embeddings_preprocessor.preprocess(data)
    elasric.disconnect()


if __name__ == '__main__':
    get_text_embeddings_params()