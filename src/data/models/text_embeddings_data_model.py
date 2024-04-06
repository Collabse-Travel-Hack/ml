from .base import BaseDataModel


class TextEmbeddingsDataModel(BaseDataModel):
    embeddings: list[float]
