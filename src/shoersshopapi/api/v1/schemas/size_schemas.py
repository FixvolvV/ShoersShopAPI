from pydantic import BaseModel


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
    size: int | None = None
    count_min: int | None = None
    count_max: int | None = None
