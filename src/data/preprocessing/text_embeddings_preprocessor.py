from data.models.text_embeddings_data_model import TextEmbeddingsDataModel
from data.preprocessing.base import PreprocessorABC
import logging

from data.utils.embedder import EmbedderABC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextEmbeddingsPreprocessor(PreprocessorABC):
    def __init__(self, storage, embedder: EmbedderABC, batch_size):
        self.storage = storage
        self.batch_size = batch_size
        self.embedder = embedder

    def preprocess(self, data):
        batch_texts = []
        batch_ids = []

        current_batch = 0

        for row in data:
            item = row.get('item')

            title = item.get('title')
            description = item.get('description')
            text = self._preprocess_text(title, description)
            batch_texts.append(text)
            batch_ids.append(item.get('id'))

            if len(batch_texts) == self.batch_size:
                logger.info(f'Processing batch {current_batch}')
                self._process_batch(batch_texts, batch_ids)
                batch_texts = []
                batch_ids = []

                current_batch += 1

        if batch_texts:
            self._process_batch(batch_texts, batch_ids)

    def _process_batch(self, batch_texts, batch_ids):
        batch_embeddings = self._extract_features(batch_texts)

        text_embeddings = []
        for i in range(len(batch_texts)):
            embeddings = TextEmbeddingsDataModel(
                id=batch_ids[i],
                embeddings=batch_embeddings[i],
            )

            text_embeddings.append(embeddings)

        self.storage.save(text_embeddings, 'embeddings')

    @staticmethod
    def _preprocess_text(title: str, description: str):
        text = title + ' ' + description
        text = text.replace('\n', ' ').replace('<br><br>', ' ').replace('<p>', '').replace('</p>', '').replace('<br>', '')
        return text

    def _extract_features(self, batch_texts):
        batch_embeddings = self.embedder.predict(batch_texts)

        return batch_embeddings
