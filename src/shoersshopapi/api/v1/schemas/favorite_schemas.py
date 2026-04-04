from pydantic import BaseModel, ConfigDict

#-------------- Favorite Schemes -------------- 

class FavoriteSchema(BaseModel):

    user_id: str
    product_id: str

class FavoriteWithId(FavoriteSchema):

    id: str

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
    product_id: str
    title: str
    price: float
    color: str
    product_logo: str | None = None
    brand_logo: str | None = None

    model_config = ConfigDict(from_attributes=True)

class FavoriteListResponse(BaseModel):
    user_id: str
    items: list[FavoriteProductResponse] = []
    total: int = 0