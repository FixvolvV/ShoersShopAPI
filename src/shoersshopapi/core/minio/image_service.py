import uuid
from fastapi import UploadFile, HTTPException, status

from .setup import s3_client
from shoersshopapi.core.settings import settings


ALLOWED_TYPES = settings.minio.allowed_type
MAX_SIZE = settings.minio.file_size * 1024 * 1024  # 5 MB


class ImageService:

    @staticmethod
    async def upload_image(file: UploadFile, folder: str, id: str) -> str:
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Недопустимый тип файла: {file.content_type}. "
                       f"Допустимые: {', '.join(ALLOWED_TYPES)}",
            )

        file_data = await file.read()

        if len(file_data) > MAX_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Файл слишком большой. Максимум: {MAX_SIZE // 1024 // 1024} MB",
            )

        ext = file.filename.split(".")[-1] if file.filename else "png"
        file_name = f"{id}.{ext}"
        file_path = f"{folder}/{file_name}"

        await s3_client.upload_file(
            file_path=file_path,
            file_data=file_data,
            content_type=file.content_type,
        )

        return file_path

    @staticmethod
    async def delete_image(file_path: str | None) -> None:
        if file_path:
            await s3_client.delete_file(file_path)

    @staticmethod
    async def replace_image(
        old_path: str | None,
        file: UploadFile,
        folder: str,
        id: str
    ) -> str:
        if old_path:
            await s3_client.delete_file(old_path)
        return await ImageService.upload_image(file, folder, id)

    @staticmethod
    async def get_image_url(file_path: str) -> str:
        return await s3_client.get_file_url(file_path)


image_service = ImageService()