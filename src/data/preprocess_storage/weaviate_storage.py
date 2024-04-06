from src.data.models.text_embeddings_data_model import TextEmbeddingsDataModel
from src.data.preprocess_storage.base import StorageABC

import weaviate.classes as wvc
import weaviate


class WeaviateStorage(StorageABC):

    def __init__(self, index_name="EmbeddingsIndex"):
        self.weaviate_client = weaviate.connect_to_local()
        self.index_name = index_name

    def save(self, data: list[TextEmbeddingsDataModel], path):
        question_objs = list()
        for item in data:
            question_objs.append(
                wvc.data.DataObject(
                    properties={"external_id": item.id},
                    vector=item.embeddings
                )
            )

        questions = self.weaviate_client.collections.get(self.index_name)
        questions.data.insert_many(question_objs)

    def load(self, path):
        pass  # Загрузка не требуется, так как данные уже будут в Weaviate

    def search(self, query_vector, top_k):

        questions = self.weaviate_client.collections.get(self.index_name)

        response = questions.query.near_vector(
            near_vector=query_vector,
            limit=top_k,
            return_metadata=wvc.query.MetadataQuery(certainty=True)
        )

        return [o.properties for o in response.objects]

    def create_index(self):
        self.weaviate_client.collections.create(
            self.index_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
            vector_index_config=wvc.config.Configure.VectorIndex.hnsw(
                distance_metric=wvc.config.VectorDistances.COSINE  # select prefered distance metric
            ),
        )
