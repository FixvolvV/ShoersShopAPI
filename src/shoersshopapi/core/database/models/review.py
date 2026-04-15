from datetime import datetime, timezone

from sqlalchemy import (
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base
from .mixin import UserRelationMixin
from shoersshopapi.core.utils.utils import get_current_df

class Review(UserRelationMixin, Base):
    _user_back_populates = "reviews"
    _user_load_strategy = "raise"

    comment_text: Mapped[str]
    rating: Mapped[int] = mapped_column(nullable=False, default=5, server_default="5")
    created_at: Mapped[datetime] = mapped_column(
        default=get_current_df,
        server_default=func.now()
    )