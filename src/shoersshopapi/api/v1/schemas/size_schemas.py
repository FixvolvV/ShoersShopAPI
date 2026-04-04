from pydantic import BaseModel, ConfigDict
from typing import List

class SizeSchema(BaseModel):
    product_id: str
    size: int
    count: int

class SizeWithId(SizeSchema):
    id: str

class SizeUpdate(BaseModel):
    count: int | None = None

class SizeFilter(BaseModel):
    id: str | None = None
    product_id: str | None = None
    size: List[int] | int | None = None
    count_min: int | None = None
    count_max: int | None = None

    model_config = ConfigDict(from_attributes=True)
