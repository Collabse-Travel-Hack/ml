from .base import PreprocessorABC
from ..database.mongo_database import MongoDatabase
from ..models.place_data_model import PlaceDataModel, ObjectTypeEnum


class PlacePreprocessor(PreprocessorABC):
    def __init__(self, storage):
        self.storage = storage

        self.mongo_db = MongoDatabase(db_name='storage', collection_name='events')
        self.mongo_db.connect()
        self.events_collection = self.mongo_db.collection
        self.places_collection = self.mongo_db.db['place_descriptions']


    @staticmethod
    def _preprocess_text(description: str):
        if description is None:
            return None

        text = description.replace('\n', ' ').replace('<br><br>', ' ').replace('<p>', '').replace('</p>', '').replace('<br>',
                                                                                                               '')
        return text

    def preprocess(self, data):
        places = []

        row_process = 0

        for row in data:

            print(f"Processing row {row_process}")
            row_process += 1

            if row.get('objectType') == ObjectTypeEnum.EVENT:
                item = self.events_collection.find_one({'item.id': {'$eq': row.get('objectId')}})
                description = item.get('item').get('description') if item and item.get('item') and item.get('item').get('description') else None

            elif row.get('objectType') == ObjectTypeEnum.PLACE:
                item = self.places_collection.find_one({'id': {'$eq': row.get('objectId')}})
                description = item.get('description') if item.get('description') else None

            else:
                description = None

            description = self._preprocess_text(description)

            place = PlaceDataModel(
                id=row.get('objectId'),
                address=row.get('address'),
                metro_station=row.get('metroStation'),
                object_type=row.get('objectType'),
                popularity=row.get('popularity'),
                title=row.get('title'),
                description=description,
                has_audio_guide=row.get('hasAudioGuide'),
                is_can_buy=row.get('isCanBuy'),
                price=row.get('price'),
                russpass_recommendation=row.get('russpassRecommendation'),
                rating=row.get('rating'),
                type=row.get('type')
            )

            places.append(place)

        print(f"Saving {len(places)} places")

        self.storage.save(places, 'places')

        self.mongo_db.disconnect()
