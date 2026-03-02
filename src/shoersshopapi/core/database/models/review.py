from sqlalchemy import (
    text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base
from .mixin import UserRelationMixin

from src.shoersshopapi.core.utils.enum import Rating


class Review(UserRelationMixin, Base):
    _user_back_populates = Base.__tablename__

    comment_text: Mapped[str]
    rating: Mapped[Rating] = mapped_column(default=Rating.very_good,  server_default=text("'very_good'"))