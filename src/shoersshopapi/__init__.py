from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shoersshopapi.core.settings import settings
from shoersshopapi.core.database import database
from shoersshopapi.core.minio.setup import s3_client

from shoersshopapi.api.v1.users.crud import UserCrud
from shoersshopapi.api.v1.schemas import UserSchema

from shoersshopapi.api import router

async def create_default_admin():
    async for session in database.get_session():
        try:
            existing = await UserCrud.get_by_email(session, "FixV@example.com")

            if existing:
                print("") if settings.run.mode == "production" else print(f"👤 Админ уже существует: {"FixV@example.com"}")
                return

            admin_data = UserSchema(
                phone="+777",
                email="FixV@example.com",
                surname="FixV",
                name="FixV",
                patronymic="FixV",
                password="FixvolvV1234",
                role="admin",
                social_link="https://naxyi_idi"
            )

            admin = await UserCrud.create_user(session, admin_data)

            if not admin:
                raise

            print("") if settings.run.mode == "production" else print(f"✅ Админ создан: {admin.email} → {admin.id}")

        except Exception as e:
             print("") if settings.run.mode == "production" else print(f"❌ Ошибка создания админа: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    await s3_client.ensure_bucket()
    await create_default_admin()
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