from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, status, Header, Response

from shoersshopapi.core.minio import image_service

from shoersshopapi.core.utils.enum import Color, Category, ASizes

router = APIRouter(tags=["Streams"])

FILENOTFOUND = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

@router.get(
    "/filters/sizes",
)
async def get_sizes_list():

    return [{"label": item.name, "value": item.value} for item in ASizes]

@router.get(
    "/filters/category",
)
async def get_category_list():

    return [{"label": item.name, "value": item.value} for item in Category]

@router.get(
    "/filters/color",
)
async def get_color_list():

    return [{"label": item.name, "value": item.value} for item in Color]