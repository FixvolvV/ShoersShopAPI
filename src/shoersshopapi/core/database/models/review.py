from sqlalchemy import (
    text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base
from .mixin import UserRelationMixin

from shoersshopapi.core.utils.enum import Rating


class Review(UserRelationMixin, Base):
    _user_back_populates = "reviews"
    _user_load_strategy = "raise"

    comment_text: Mapped[str]
    rating: Mapped[Rating] = mapped_column(default=Rating.very_good,  server_default=text("'very_good'"))