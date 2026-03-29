from pydantic import BaseModel
from typing import (
    Optional,
    Sequence
)

from shoersshopapi.core.utils.enum import Rating

#-------------- Review Schemes -------------- 

class ReviewSchema(BaseModel):

    comment_text: str
    rating: Rating | str

class ReviewWithId(ReviewSchema):

    id: str
    user_id: str

class ReviewUpdate(BaseModel):
    comment_text: str | None = None
    rating: Rating | None = None

class ReviewsSchema(BaseModel):

    reviews: Optional[Optional[ReviewWithId]] = None

#-------------- Review Filters --------------

class ReviewFilter(BaseModel):

    id: str | None = None
    user_id: str | None = None
    comment_text: str | None = None
    rating: Rating | str | None = None
