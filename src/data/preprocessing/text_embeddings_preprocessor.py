from typing import List

from src.data.models.place_data_model import PlaceDataModel
from src.data.models.text_embeddings_data_model import TextEmbeddingsDataModel
from src.data.preprocessing.base import PreprocessorABC
import logging

import re


from src.data.utils.embedder import EmbedderABC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextEmbeddingsPreprocessor(PreprocessorABC):
    def __init__(self, storage, embedder: EmbedderABC, batch_size):
        self.storage = storage
        self.batch_size = batch_size
        self.embedder = embedder

    def preprocess(self, data: List[dict]):
        batch_texts = []
        batch_ids = []

        current_batch = 0

        for row in data:

            place = PlaceDataModel(**row)


            text_data = []
            if place.description:
                text_data.append(place.description)
            if place.title:
                text_data.append(place.title)
            if place.address:
                text_data.append(place.address)
            if place.metro_station:
                text_data.append(place.metro_station)
            if place.type:
                text_data.append(place.type)

            text = self._preprocess_text(text_data)
            batch_texts.append(text)
            batch_ids.append(place.id)

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

        self.storage.save(text_embeddings, path=None)

    @staticmethod
    def _preprocess_text(text_data: List[str]):
        if text_data is None:
            return None

        text = ' '.join(text_data)

        # Удаление HTML-тегов
        text = re.sub(r'<[^>]*>', '', text)

        # Удаление ссылок
        text = re.sub(r'http\S+', '', text)

        # Удаление времени в формате xx:xx
        text = re.sub(r'\d{2}:\d{2}', '', text)

        return text

    def _extract_features(self, batch_texts):
        batch_embeddings = self.embedder.predict(batch_texts)

        return batch_embeddings
