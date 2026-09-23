print("JAI SHRIRAM")

from io import BytesIO


from minio import Minio

from app.core.config import settings


class MinIOStorage:
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )

        self.bucket = settings.minio_bucket

        self._ensure_bucket()

    def _ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def object_exists(self, object_name: str) -> bool:
        try:
            self.client.stat_object(
                self.bucket,
                object_name,
            )
            return True
        except Exception:
            return False

    def upload_bytes(
        self,
        object_name: str,
        data: bytes,
    ):
        self.client.put_object(
            self.bucket,
            object_name,
            BytesIO(data),
            length=len(data),
        )

    def download_bytes(self, object_name: str) -> bytes:
        response = self.client.get_object(
        self.bucket,
        object_name,
    )

        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()
            