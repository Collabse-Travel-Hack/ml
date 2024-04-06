from pydantic import BaseModel


class BaseDataModel(BaseModel):
    id: str
    class Config:
        from_attributes = True
