from typing import List
from pydantic import BaseModel, ConfigDict

#-------------- Brand Schemes -------------- 

class BrandSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    brand_name: str
    brand_logo: str

class BrandWithId(BrandSchema):

    model_config = ConfigDict(from_attributes=True)

    id: str

class BrandUpdate(BaseModel):
    brand_name: str | None = None
    brand_logo: str | None = None


#-------------- Brand Filters -------------- 

class BrandFilter(BaseModel):
    id: str | None = None
    brand_name: List[str] | None = None

    model_config = ConfigDict(from_attributes=True)
