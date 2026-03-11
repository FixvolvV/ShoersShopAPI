from shoersshopapi.api.v1.basecrud import BaseCrud

from shoersshopapi.core.database.models import User

class UserCrud(BaseCrud[User]):
    model = User
