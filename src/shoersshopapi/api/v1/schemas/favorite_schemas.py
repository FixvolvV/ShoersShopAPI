from pydantic import BaseModel, ConfigDict

from .product_schemas import ProductWithAll

#-------------- Favorite Schemes -------------- 

class FavoriteSchema(BaseModel):

    user_id: str
    product_id: str

class FavoriteWithId(FavoriteSchema):

    id: str

    model_config = ConfigDict(from_attributes=True)

class FavoriteAdd(BaseModel):
    product_id: str

class FavoriteUpdate(BaseModel):

    user_id: str | None = None
    product_id: str | None = None

#-------------- Favorite Filters -------------- 

class FavoriteFilter(BaseModel):

    id: str | None = None
    user_id: str | None = None
    product_id: str | None = None

#-------------- Favorite Forms --------------

class FavoriteProductResponse(BaseModel):
    id: str
    product: ProductWithAll

    model_config = ConfigDict(from_attributes=True)

class FavoriteListResponse(BaseModel):
    user_id: str
    items: list[FavoriteProductResponse] = []
    total: int = 0