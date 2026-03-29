from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database import database
from .crud import BrandCrud

from shoersshopapi.api.v1.schemas import BrandWithId, BrandFilter, UserWithId

from shoersshopapi.api.v1.validators.http import (
    oauth2_scheme,
    get_current_auth_user,
    RoleRequired,
)

router = APIRouter(
        tags=["Brands"],
        dependencies=[Depends(oauth2_scheme)]
)

BRANDNOTFOUND = HTTPException(
    status_code=404,
    detail="Brand not found"
)

@router.post(
    "/",
    response_model=BrandWithId,
    status_code=status.HTTP_201_CREATED,
)
async def create_brand(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    name: str,
    logo: Annotated[
        UploadFile,
        File(...)
    ]
):
    brand = await BrandCrud.create_brand(session, brand_name=name, brand_logo=logo)
    return brand


@router.get(
    "/{brand_id}",
    response_model=BrandWithId,
    summary="Получить бренд по ID",
)
async def get_brand(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    brand_id: str,
):
    brand = await BrandCrud.get_by_id(session, brand_id)

    if not brand:
        raise BRANDNOTFOUND

    return brand


@router.get(
    "/",
    response_model=list[BrandWithId],
    summary="Получить список брендов",
)
async def get_brands(
    user: Annotated[
        UserWithId,
        Depends(get_current_auth_user)
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    brands = await BrandCrud.get_all(
        session,
        limit=limit,
        offset=(page - 1) * limit,
    )
    return brands


@router.patch(
    "/{brand_id}",
    response_model=BrandWithId,
)
async def update_brand_logo(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    brand_id: str,
    brand_name: str | None,
    logo: Annotated[
        UploadFile | None,
        File(...)
    ]
):

    if not brand_name and not logo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нужно передать хотя бы одно поле для обновления",
        )

    brand = await BrandCrud.update_brand(session, brand_id, brand_name, logo)

    if not brand:
        raise BRANDNOTFOUND

    return brand


@router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_brand(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    brand_id: str,
):
    deleted = await BrandCrud.delete_brand(session, brand_id)

    if not deleted:
        raise BRANDNOTFOUND