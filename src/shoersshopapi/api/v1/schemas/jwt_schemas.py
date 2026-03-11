from pydantic import BaseModel
from shoersshopapi.core.utils.enum import Role

class JWTCreateSchema(BaseModel):

    id: str
    username: str
    password: str
    role: Role

class TokenInfo(BaseModel):
    
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"