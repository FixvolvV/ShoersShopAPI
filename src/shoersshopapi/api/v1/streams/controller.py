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
    "/images",
)
async def get_image_redirect(
    path: str,
    if_none_match: Annotated[
        Optional[str],
        Header()
    ]
):

    # Валидация пути (безопасность)
    if ".." in path or path.startswith("/") or len(path) > 255:
        raise HTTPException(
            status_code=400, 
            detail="Некорректный путь к файлу"
        )
    
    # Генерируем ETag для кэширования
    etag = f'"{image_service.get_image_etag(path)}"'
    
    # Если клиент уже имеет актуальную версию
    if if_none_match == etag:
        return Response(status_code=304)  # Not Modified
    
    try:
        # Получаем presigned URL (1 час действия)
        presigned_url = await image_service.get_redirect_url(
            file_path=path,
            expires_in=3600  # 1 час
        )
        
        # Редиректим на S3
        return Response(
            status_code=307,  # Temporary Redirect (сохраняет метод GET)
            headers={
                "Location": presigned_url,
                "Cache-Control": "public, max-age=3000",  # 50 минут (меньше чем expires_in)
                "ETag": etag,
                "X-Redirect-Type": "s3-presigned",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера {e}"
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