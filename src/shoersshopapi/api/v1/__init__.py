from fastapi import APIRouter

from shoersshopapi.api.v1.users.controller import router as users_router


router = APIRouter(prefix="/v1")

router.include_router(users_router, prefix="/users")