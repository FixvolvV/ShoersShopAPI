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

        async with s3_client.get_client() as client:
            await client.put_object(
                Bucket=settings.minio.bucket_name,
                Key=file_path,
                Body=file_data,
                ContentType=file.content_type,
            )

        return file_path

    @staticmethod
    async def delete_image(file_path: str | None) -> None:
        if file_path:
            async with s3_client.get_client() as client:
                await client.delete_object(
                    Bucket=settings.minio.bucket_name,
                    Key=file_path
                )

    @staticmethod
    async def replace_image(
        old_path: str | None,
        file: UploadFile,
        folder: str,
        id: str
    ) -> str:
        if old_path:
            async with s3_client.get_client() as client:
                await client.delete_object(
                    Bucket=settings.minio.bucket_name,
                    Key=old_path
                )
        return await ImageService.upload_image(file, folder, id)

    @staticmethod
    async def get_image_url(file_path: str,  expires_in: int = 3600) -> str:
        async with s3_client.get_client() as client:
            url = await client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.minio.bucket_name,
                'Key': file_path
            },
            ExpiresIn=expires_in
        )

        url = url.replace(s3_client.endpoint_url, s3_client.external_endpoint)

        return url

    @staticmethod
    def get_image_etag(file_path: str) -> str:
        return s3_client.get_file_etag(file_path)

image_service = ImageService()