print("JAI SHRIRAM")

from app.storage.minio_storage import MinIOStorage


storage = MinIOStorage()

storage.upload_bytes(
    "test.txt",
    b"Hello from Chronix!"
)

print("Upload successful!")