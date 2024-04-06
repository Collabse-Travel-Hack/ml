from fastapi import HTTPException, Query, APIRouter
from pydantic import BaseModel

from src.data.database.elastic_search_database import ElasticDatabase
from src.data.preprocess_storage.weaviate_storage import WeaviateStorage
from src.data.utils.embedder import RuBERTEmbedder

router = APIRouter()

storage = WeaviateStorage()
embedder = RuBERTEmbedder()
# elastic = ElasticDatabase(host='http://158.160.14.223:9200')
# elastic.connect()


class GetSimilarRequest(BaseModel):
    text: str
    top_k: int = Query(5, ge=1, le=10)


@router.post("/get_similarr")
async def get_similar_handler(request: GetSimilarRequest):
    try:
        query_vector = embedder.predict([request.text])[0].tolist()
        similar_places = storage.search(query_vector, top_k=request.top_k)

        if not similar_places:
            raise HTTPException(status_code=404, detail="Record not found")

        results = []

        for place in similar_places:
            results.append([1, 2, 3])

        return "results"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
