from enum import StrEnum

from src.data.models.base import BaseDataModel
from pydantic import Field, Extra
from typing import Optional


class ObjectTypeEnum(StrEnum):
    PLACE = 'PLACE'
    EVENT = 'EVENT'
    RESTAURANT = 'RESTAURANT'
    TRACK = 'TRACK'
    EXCURSION = 'EXCURSION'


class PlaceDataModel(BaseDataModel):
    address: Optional[str] = Field(None)
    metro_station: Optional[str] = Field(None)
    object_type: ObjectTypeEnum
    popularity: float
    title: str
    description: Optional[str] = Field(None)
    has_audio_guide: Optional[bool] = Field(None)
    is_can_buy: Optional[bool] = Field(None)
    price: Optional[float] = Field(None)
    russpass_recommendation: Optional[bool] = Field(None)
    rating: Optional[float] = Field(None)
    type: Optional[str] = Field(None)

    class Config:
        str_strip_whitespace = True
        str_min_length = 0
        extra = Extra.allow
