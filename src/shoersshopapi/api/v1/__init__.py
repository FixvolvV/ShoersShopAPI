from fastapi import APIRouter

from shoersshopapi.api.v1.auth.controller import router as auth_router
from shoersshopapi.api.v1.users.controller import router as users_router
from shoersshopapi.api.v1.brands.controller import router as brands_router
from shoersshopapi.api.v1.products.controller import router as products_router
from shoersshopapi.api.v1.sizes.controller import router as sizes_router
from shoersshopapi.api.v1.favorite.controller import router as favorite_router
from shoersshopapi.api.v1.orders.controller import router as orders_router
from shoersshopapi.api.v1.carts.controller import router as carts_router
from shoersshopapi.api.v1.addresses.controller import router as addresses_router
from shoersshopapi.api.v1.reviews.controller import router as reviews_router

from shoersshopapi.api.v1.streams.controller import router as streams_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router, prefix="/auth")
router.include_router(users_router, prefix="/users")
router.include_router(brands_router, prefix="/brands")
router.include_router(products_router, prefix="/products")
router.include_router(sizes_router, prefix="/sizes")
router.include_router(favorite_router, prefix="/favorites")
router.include_router(orders_router, prefix="/orders")
router.include_router(carts_router, prefix="/carts")
router.include_router(addresses_router, prefix="/addresses")
router.include_router(reviews_router, prefix="/reviews")

router.include_router(streams_router, prefix="/streams")