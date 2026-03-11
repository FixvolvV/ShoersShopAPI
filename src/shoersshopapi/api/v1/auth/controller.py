from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from shoersshopapi.api.v1.schemas import TokenInfo


router = APIRouter(
    tags=["Authentication"],
    prefix="/auth",
    )




