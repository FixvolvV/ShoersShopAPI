from pydantic import BaseModel

from shoersshopapi.core.utils.enum import Color
from .brand_schemas import BrandWithId

#-------------- Product Schemas -------------- 

class ProductSchema(BaseModel):
    brand_id: str
    title: str
    price: float
    color: Color
    logo: str
    avg_grade: str | None = None

class ProductWithId(ProductSchema):
    id: str

class ProductWithBrand(ProductWithId):
    brand: BrandWithId

class ProductUpdate(BaseModel):
    title: str | None = None
    price: float | None = None
    color: Color | None = None
    logo: str | None = None
    avg_grade: str | None = None

#-------------- Product Filters -------------- 

class ProductFilter(BaseModel):
    id: str | None = None
    title: str | None = None
    color: Color | None = None
    price_min: float | None = None
    price_max: float | None = None

#-------------- Product Forms -------------- 

class ProductCreate(BaseModel):
    brand_id: str
    title: str
    price: float
    color: Color
    avg_grade: str | None = None