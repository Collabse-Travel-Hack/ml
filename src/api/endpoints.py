from fastapi import HTTPException, Query, APIRouter
from pydantic import BaseModel

from src.data.utils.embedder import RuBERTEmbedder
from src.data.utils.gigachat_api import GigachatAPI
# from src.api.model import embedder
from src.config.settings import ELASTICSEARCH_HOST, WEAVIATE_HOST, GIGACHAT_HOST
from src.data.database.elastic_search_database import ElasticDatabase
from src.data.preprocess_storage.weaviate_storage import WeaviateStorage


router = APIRouter()

storage = WeaviateStorage(host=WEAVIATE_HOST)
elastic_db = ElasticDatabase(host=ELASTICSEARCH_HOST)
elastic_db.connect()

embedder = RuBERTEmbedder()


gigachat_api = GigachatAPI(host=GIGACHAT_HOST)


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
            results.append(elastic_db.find(index='places', query={"query": {"match": {"id": place['external_id']}}})[0])

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
    TOP_N = 3

    try:
        query = {
            "query": {
                "match": {
                    "type": request.type
                }
            },
            "aggs": {
                "top_n_by_popularity": {
                    "terms": {
                        "field": "popularity",
                        "size": TOP_N,
                        "order": {
                            "_count": "desc"
                        }
                    }
                }
            }
        }

        results = elastic_db.find(index='places', query=query)

        if not results:
            raise HTTPException(status_code=404, detail="Records not found")

        descriptions = [place.get('description') for place in results]
        titles = [place.get('title') for place in results]

        prompt = generate_prompt(descriptions, titles, request.text)
        response = gigachat_api.ask("", prompt)

        return response

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def generate_prompt(descriptions, titles, keywords):
    prompt = "Документы с наибольшей популярностью:\n\n"

    for i, (title, description) in enumerate(zip(titles, descriptions), start=1):
        prompt += f"Документ {i}:\nTitle: {title}\nDescription: {description}\n\n"

    prompt += (
        f"Используя приведенные выше популярные документы в качестве примера "
        f"и основываясь на ключевых словах '{keywords}', "
        f"сгенерируйте новый title и description:\n\n"
    )

    return prompt