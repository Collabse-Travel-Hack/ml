from src.data.models.base import BaseDataModel
from pydantic import Field, Extra
from typing import Optional


class EventDataModel(BaseDataModel):
    duration: int
    is_can_buy: bool
    russpass_recommendation: bool
    event_type: str | None
    payment_method: str | None
    type_audio_guides: str | None
    city: str | None
    metro: str | None
    general_rating: Optional[float] = Field(None)
    marks_count: Optional[int] = Field(None)
    publication_date: Optional[str] = Field(None)
    min_age: Optional[int] = Field(None)
    ticket_price: Optional[float] = Field(None)
    tags: Optional[list] = Field(default_factory=list)
    sentiment: Optional[float] = Field(None)
    flesch_reading_ease: Optional[float] = Field(None)
    text_length: Optional[int] = Field(None)

    class Config:
        str_strip_whitespace = True
        str_min_length = 0
        extra = Extra.allow
