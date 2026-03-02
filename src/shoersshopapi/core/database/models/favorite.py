from src.shoersshopapi.core.database.models.mixin import UserRelationMixin

from .base import Base

class Favorite(UserRelationMixin, Base):
    _user_back_populates = Base.__tablename__
