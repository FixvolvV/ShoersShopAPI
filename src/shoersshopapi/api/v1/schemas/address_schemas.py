from pydantic import BaseModel, ConfigDict
from typing import (
    Optional,
    Sequence
)

#-------------- Address Schemes -------------- 

class AddressSchema(BaseModel):
    
    region: str
    city: str
    street: str
    house: str
    entrance: str
    apartment: str
    postcode: int

class AddressWithId(AddressSchema):

    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)

class AddressesSchema(BaseModel):

    addresses: Optional[Optional[AddressWithId]] = None

class AddressUpdate(BaseModel):
    
    region: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    entrance: str | None = None
    apartment: str | None = None
    postcode: int | None = None

#-------------- Address Filter -------------- 

class AddressFilter(BaseModel):
    
    id: str | None = None
    user_id: str | None = None
    region: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    entrance: str | None = None
    apartment: str | None = None
    postcode: int | None = None