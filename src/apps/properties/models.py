from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField
from bson.objectid import ObjectId


class Property(BaseModel):
    id: int | ObjectIdField = Field(alias="_id")
    name: str
    image: str | None

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
        allow_population_by_filed_name = True


class PropertyInput(BaseModel):
    name: str = Field(min_length=3, max_length=5)
    image: str | None = None
