from pydantic import BaseModel

#-------------- Favorite Schemes -------------- 

class FavoriteSchema(BaseModel):

    user_id: str
    product_id: str

class FavoriteWithId(FavoriteSchema):

    id: str

class FavoriteUpdate(BaseModel):

    user_id: str | None = None
    product_id: str | None = None

#-------------- Favorite Filters -------------- 

class FavoriteFilter(BaseModel):

    id: str | None = None
    user_id: str | None = None
    product_id: str | None = None