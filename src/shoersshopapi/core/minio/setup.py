import hashlib

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aioboto3
from botocore.exceptions import ClientError

from shoersshopapi.core.settings import settings

class MinioClient:

    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region_name: str = "us-east-1",
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region_name = region_name
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator:
        session = aioboto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
        )

        async with session.client(  # type: ignore
            "s3",
            endpoint_url=self.endpoint_url,
        ) as client:
            yield client

    async def ensure_bucket(self) -> None:
        async with self.get_client() as client:
            try:
                await client.head_bucket(Bucket=self.bucket_name)
            except ClientError:
                await client.create_bucket(Bucket=self.bucket_name)

    def get_file_etag(self, file_path: str) -> str:
        return hashlib.md5(file_path.encode()).hexdigest()


s3_client = MinioClient(
    endpoint_url=settings.minio.endpoint_url,
    access_key=settings.minio.access_key,
    secret_key=settings.minio.secret_key,
    bucket_name=settings.minio.bucket_name,
    region_name=settings.minio.region_name,
)