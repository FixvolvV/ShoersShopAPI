from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shoersshopapi.core.database.models import Review, Order, Cart, Favorite
from shoersshopapi.core.settings import settings

from shoersshopapi.api import router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    yield
    # shutdown

app = FastAPI(
    lifespan=lifespan,
    docs_url=None if settings.run.mode == "production" else "/docs", #disables docs
    redoc_url=None if settings.run.mode == "production" else "/redoc", #disables redoc
    openapi_url=None if settings.run.mode == "production" else "/openapi.json", #disables openapi.json suggested by tobias comment.
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.httpcors.urls, #pyright:ignore
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)