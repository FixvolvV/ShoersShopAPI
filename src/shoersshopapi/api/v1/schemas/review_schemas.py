from pydantic import BaseModel, ConfigDict, model_validator
from typing import (
    Optional,
    Sequence
)
from datetime import datetime

#-------------- Review Schemes -------------- 

class ReviewSchema(BaseModel):

    comment_text: str
    rating: int
    created_at: datetime

    @model_validator(mode='after')
    def raiting_value_check(self):
        if self.rating not in range(1,6):
            raise ValueError("Raiting out of range")
        return self

class ReviewWithId(ReviewSchema):

    id: str
    user_id: str

    model_config = ConfigDict(from_attributes=True)

class ReviewUpdate(BaseModel):
    comment_text: str | None = None
    rating: int | None = None
    created_at: datetime | None = None

    @model_validator(mode='after')
    def raiting_value_check(self):
        if self.rating != None and self.rating not in range(1,6):
            raise ValueError("Raiting out of range")
        return self

class ReviewsSchema(BaseModel):

    reviews: Optional[Optional[ReviewWithId]] = None

#-------------- Review Filters --------------

class ReviewFilter(BaseModel):

    id: str | None = None
    user_id: str | None = None
    comment_text: str | None = None
    rating: int | None = None
    created_at: datetime | None = None
    
