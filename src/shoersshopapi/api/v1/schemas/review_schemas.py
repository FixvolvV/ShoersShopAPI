from pydantic import BaseModel
from typing import (
    Sequence
)

from shoersshopapi.core.utils.enum import Rating

#-------------- Review Schemes -------------- 

class ReviewSchema(BaseModel):

    user_id: str
    comment_text: str
    rating: Rating

class ReviewWithId(BaseModel):

    id: str

class ReviewsSchema(BaseModel):

    reviews: Sequence[ReviewWithId | None] | None

#-------------- Review Filters --------------

class ReviewFilter(BaseModel):

    id: str | None = None
    user_id: str | None = None
    comment_text: str | None = None
    rating: Rating | None = None