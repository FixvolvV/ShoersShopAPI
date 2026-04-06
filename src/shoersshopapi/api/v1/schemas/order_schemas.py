from pydantic import BaseModel, ConfigDict
from typing import (
    Optional
)
from datetime import datetime

from shoersshopapi.core.utils.enum import Status
from .address_schemas import AddressWithId


#-------------- Order Schemes -------------- 

class OrderSchema(BaseModel):
    
    address_id: str
    order_date: datetime
    total_amount: float
    status: Status

class OrderWithId(OrderSchema):

    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)

class OrdersSchema(BaseModel):

    orders: Optional[Optional[OrderWithId]] = None

class OrderUpdate(BaseModel):

    order_date: str | None = None
    total_amount: float | None = None
    status: Status | None = None


#-------------- Order Filters -------------- 

class OrderFilter(BaseModel):

    id: str | None = None
    address_id: str | None = None
    user_id: str | None = None
    order_date: str | None = None
    total_amount: float | None = None
    status: Status | str | None = None

#-------------- Order Forms -------------- 

class OrderCreate(BaseModel):
    address_id: str

class OrderItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int

class OrderItemWithProduct(BaseModel):
    id: str
    product_id: str
    quantity: int
    title: str
    price: float

class OrderItemData(BaseModel):
    id: str
    order_id: str
    product_id: str
    quantity: int

class OrderWithItems(OrderWithId):
    items: list[OrderItemResponse] = []
    address: AddressWithId | None = None


class OrderFull(OrderWithId):
    items: list[OrderItemWithProduct] = []
    address: AddressWithId | None = None