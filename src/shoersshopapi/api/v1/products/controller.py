from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession

from shoersshopapi.api.v1.schemas.size_schemas import SizeFilter
from shoersshopapi.core.database import database
from shoersshopapi.core.utils.enum import Color

from .crud import ProductCrud
from shoersshopapi.api.v1.schemas import (
    ProductWithAll,
    ProductWithId,
    ProductUpdate,
    ProductFilter,
    ProductWithBrand,
    BrandFilter,
    UserWithId,
    ProductCreate
)

from shoersshopapi.api.v1.validators.http import (
    RoleRequired,
)


router = APIRouter(
    tags=["Products"]
)


PRODUCTNOTFOUND = HTTPException(
    status_code=404,
    detail="Product not found"
)

@router.post(
    "/",
    response_model=ProductWithId,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    data: ProductCreate
):

    product = await ProductCrud.create_product(session, data)
    return product


@router.get(
    "/{product_id}",
    response_model=ProductWithAll,
    summary="Получить продукт по ID",
)
async def get_product(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    product_id: str,
):
    product = await ProductCrud.get_by_id(session, product_id)

    if not product:
        raise PRODUCTNOTFOUND

    return product


@router.get(
    "/",
    response_model=list[ProductWithAll],
    summary="Получить список продуктов",
)
async def get_products(
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    # Фильтры продукта
    title: str | None = None,
    color: Color | None = None,
    brand_name: str | None = None,
    size: Annotated[list[int] | None, Query()] = None,
    article: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    # Пагинация
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    product_filters = ProductFilter(
        title=title,
        color=color,
        article=article,
        price_min=price_min,
        price_max=price_max,
    )

    brand_filters = BrandFilter(
        brand_name=brand_name
    )

    size_filters = SizeFilter(
        size=size
    )

    products = await ProductCrud.get_all(
        session,
        filters=product_filters,
        brand_filters=brand_filters,
        size_filters=size_filters,
        limit=limit,
        offset=(page - 1) * limit,
    )

    return products


@router.patch(
    "/{product_id}",
    response_model=ProductUpdate,
)
async def update_product(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    product_id: str,
    data: ProductUpdate,
):
    product = await ProductCrud.update_product(session, product_id, data)

    if not product:
        raise PRODUCTNOTFOUND

    return product

@router.patch(
    "/logo/{product_id}",
    response_model=ProductUpdate,
)
async def update_product_logo(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    product_id: str,
    logo: Annotated[
        UploadFile,
        File(...)
    ]
):
    product = await ProductCrud.update_product_logo(session, product_id, logo)

    if not product:
        raise PRODUCTNOTFOUND

    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    user: Annotated[
        UserWithId,
        Depends(RoleRequired("admin"))
    ],
    session: Annotated[
        AsyncSession,
        Depends(database.get_session)
    ],
    product_id: str,
):
    deleted = await ProductCrud.delete_product(session, product_id)

    if not deleted:
        raise PRODUCTNOTFOUND