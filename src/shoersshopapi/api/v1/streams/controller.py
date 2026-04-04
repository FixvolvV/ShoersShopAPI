from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from io import BytesIO

from shoersshopapi.core.minio import s3_client

router = APIRouter(tags=["Streams"])

FILENOTFOUND = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

@router.get(
    "/",
)
async def get_file(path: str):

    exists = await s3_client.file_exists(path)
    if not exists:
        raise FILENOTFOUND

    file_data = await s3_client.get_file(path)

    ext = path.rsplit(".", 1)[-1].lower()
    content_types = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
    }
    content_type = content_types.get(ext, "application/octet-stream")

    return StreamingResponse(
        BytesIO(file_data),
        media_type=content_type,
    )