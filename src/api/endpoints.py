from fastapi import HTTPException, Query, APIRouter
from pydantic import BaseModel

from src.api.model import embedder
from src.config.settings import ELASTICSEARCH_HOST, WEAVIATE_HOST
from src.data.database.elastic_search_database import ElasticDatabase
from src.data.preprocess_storage.weaviate_storage import WeaviateStorage

router = APIRouter()

storage = WeaviateStorage(host=WEAVIATE_HOST)
elastic = ElasticDatabase(host=ELASTICSEARCH_HOST)
elastic.connect()


class GetSimilarRequest(BaseModel):
    text: str
    top_k: int = Query(5, ge=1, le=10)


@router.post("/get_similar")
async def get_similar_handler(request: GetSimilarRequest):
    try:
        query_vector = embedder.predict([request.text])[0].tolist()
        similar_places = storage.search(query_vector, top_k=request.top_k)

        if not similar_places:
            raise HTTPException(status_code=404, detail="Record not found")

        results = []

        for place in similar_places:
            results.append(elastic.find(index='places', query={"query": {"match": {"id": place['external_id']}}})[0])

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_index")
async def delete_index_handler():
    try:
        storage.delete_index()
        return {"message": "Index deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class GenerateCardRequest(BaseModel):
    text: str
    type: str


@router.post("/generate_card")
async def generate_card_handler(request: GenerateCardRequest):
    top_n = 3

    try:

        query = {
            "query": {
                "match": {
                    "type": request.type
                }
            },
        }


        result = elastic.find(index='places', query=query)

        return result

        if not result:
            raise HTTPException(status_code=404, detail="Record not found")

        return result

        buckets = result['aggregations']['top_n_by_popularity']['buckets']

        descriptions = []
        titles = []
        for bucket in buckets:
            top_hit = bucket['top_hits']['hits']['hits'][0]['_source']
            description = top_hit.get('description', '')
            title = top_hit.get('title', '')
            descriptions.append(description)
            titles.append(title)


        return {
            "titles": titles,
            "descriptions": descriptions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
