from pydantic import BaseModel
from typing import (
    Sequence
)

from shoersshopapi.core.utils.enum import Status


#-------------- Order Schemes -------------- 

class OrderSchema(BaseModel):
    
    address_id: int
    user_id: str
    order_date: str
    total_amount: float
    status: Status

class OrderWithId(OrderSchema):

    id: str

class OrdersSchema(BaseModel):

    orders: Sequence[OrderWithId | None] | None

class OrderUpdate(BaseModel):

    order_date: str | None = None
    total_amount: float | None = None
    status: Status | None = None

#-------------- Order Filters -------------- 

class OrderFilter(BaseModel):

    id: str | None = None
    address_id: int | None = None
    user_id: str | None = None
    order_date: str | None = None
    total_amount: float | None = None
    status: Status | None = None