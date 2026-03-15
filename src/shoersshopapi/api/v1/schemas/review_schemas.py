from pydantic import BaseModel
from typing import (
    Optional,
    Sequence
)

from shoersshopapi.core.utils.enum import Rating

#-------------- Review Schemes -------------- 

class ReviewSchema(BaseModel):

    user_id: str
    comment_text: str
    rating: Rating | str

class ReviewWithId(BaseModel):

    id: str

class ReviewsSchema(BaseModel):

    reviews: Optional[Optional[ReviewWithId]] = None

#-------------- Review Filters --------------

class ReviewFilter(BaseModel):

    id: str | None = None
    user_id: str | None = None
    comment_text: str | None = None
    rating: Rating | str | None = None