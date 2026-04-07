from pydantic import BaseModel, ConfigDict, model_validator

from typing import List

from pydantic_core.core_schema import model_field

from shoersshopapi.core.utils.enum import Color
from .brand_schemas import BrandWithId
from .size_schemas import SizeWithId

#-------------- Product Schemas -------------- 

class ProductSchema(BaseModel):
    brand_id: str
    title: str
    price: float
    color: Color
    logo: str | None = None
    category: str
    article: str
    avg_grade: float

class ProductWithId(ProductSchema):
    id: str

class ProductWithBrand(ProductWithId):
    brand: BrandWithId

class ProductWithAll(ProductWithBrand):
    sizes: List[SizeWithId] | None = None
    avaliable_sizes: List[SizeWithId] | None = None

    @model_validator(mode="after")
    def filter_available_sizes(self):
        if self.sizes:
            self.avaliable_sizes = [size for size in self.sizes if size.count > 0]
        return self
    
class ProductUpdate(BaseModel):
    title: str | None = None
    price: float | None = None
    color: Color | None = None
    logo: str | None = None
    article: str | None = None
    category: str | None = None
    avg_grade: float | None = None

#-------------- Product Filters -------------- 

class ProductFilter(BaseModel):
    id: str | None = None
    title: str | None = None
    color: Color | None = None
    article: str | None = None
    category: str | None = None
    price_min: float | None = None
    price_max: float | None = None

    model_config = ConfigDict(from_attributes=True)

#-------------- Product Forms -------------- 

class ProductCreate(BaseModel):
    brand_id: str
    title: str
    price: float
    color: Color
    article: str
    category: str
    avg_grade: float