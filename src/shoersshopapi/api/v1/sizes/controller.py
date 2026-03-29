from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.core.database import database
from .crud import SizeCrud
from shoersshopapi.api.v1.schemas import (
    SizeSchema,
    SizeUpdate,
    SizeWithId
)

router = APIRouter(tags=["Sizes"])

SIZENOTFOUND = HTTPException(status_code=404, detail="Size not found")

@router.post(
    "/",
    response_model=SizeWithId,
    status_code=status.HTTP_201_CREATED,
)
async def create_size(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    data: SizeSchema,
):
    size = await SizeCrud.create_size(session, data)
    return size


@router.get(
    "/product/{product_id}",
    response_model=list[SizeWithId],
    summary="Получить все размеры товара",
)
async def get_product_sizes(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    product_id: str,
):
    sizes = await SizeCrud.get_by_product(session, product_id)
    return sizes


@router.get(
    "/product/{product_id}/available",
    response_model=list[SizeWithId],
    summary="Получить размеры в наличии",
)
async def get_available_sizes(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    product_id: str,
):
    sizes = await SizeCrud.get_available_by_product(session, product_id)
    return sizes


@router.get(
    "/{size_id}",
    response_model=SizeWithId,
    summary="Получить размер по ID",
)
async def get_size(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    size_id: str,
):
    size = await SizeCrud.get_by_id(session, size_id)

    if not size:
        raise SIZENOTFOUND

    return size


@router.patch(
    "/{size_id}",
    response_model=SizeWithId
)
async def update_size(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    size_id: str,
    data: SizeUpdate,
):
    size = await SizeCrud.update_size(session, size_id, data)

    if not size:
        raise SIZENOTFOUND

    return size


@router.delete(
    "/{size_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_size(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    size_id: str,
):
    deleted = await SizeCrud.delete_size(session, size_id)

    if not deleted:
        raise SIZENOTFOUND