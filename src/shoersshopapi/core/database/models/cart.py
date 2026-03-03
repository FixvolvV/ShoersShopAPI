from shoersshopapi.core.database.models.mixin import UserRelationMixin

from .base import Base

class Cart(UserRelationMixin, Base):
    _user_back_populates = Base.__tablename__
    _user_id_unique = True