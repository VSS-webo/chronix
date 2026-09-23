print("JAI SHRIRAM")

# import hashlib
# import json

# import polars as pl
# from sqlalchemy.orm import Session

# from app.models.dataset import Dataset
# from app.storage.minio_storage import MinIOStorage


# storage = MinIOStorage()


# def calculate_sha256(data: bytes) -> str:
#     """
#     Calculate SHA-256 hash of the uploaded file.
#     """
#     sha256 = hashlib.sha256()
#     sha256.update(data)

#     return sha256.hexdigest()


# def get_dataset_metadata(data: bytes) -> dict:
#     """
#     Extract basic metadata from a CSV dataset.
#     """

#     df = pl.read_csv(data)

#     schema = {
#         column: str(dtype)
#         for column, dtype in df.schema.items()
#     }

#     return {
#         "row_count": df.height,
#         "column_count": df.width,
#         "schema": json.dumps(schema),
#     }


# def create_dataset(
#     db: Session,
#     repository_id: int,
#     filename: str,
#     data: bytes,
# ) -> Dataset:

#     # 1. Calculate content hash
#     file_hash = calculate_sha256(data)

#     # 2. Use the hash as the MinIO object name
#     object_name = file_hash

#     # 3. Upload only if this object does not already exist
#     if not storage.object_exists(object_name):
#         storage.upload_bytes(
#             object_name,
#             data,
#         )

#     # 4. Extract dataset metadata
#     metadata = get_dataset_metadata(data)

#     # 5. Store metadata in PostgreSQL
#     dataset = Dataset(
#         repository_id=repository_id,
#         name=filename,
#         object_hash=file_hash,
#         file_size=len(data),
#         row_count=metadata["row_count"],
#         column_count=metadata["column_count"],
#         schema=metadata["schema"],
#     )

#     db.add(dataset)
#     db.commit()
#     db.refresh(dataset)

#     return dataset

print("JAI SHRIRAM")


import hashlib
import json

import polars as pl
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.models.dataset_version import DatasetVersion
from app.storage.minio_storage import MinIOStorage


storage = MinIOStorage()


def calculate_sha256(data: bytes) -> str:
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()


def get_dataset_metadata(data: bytes) -> dict:
    df = pl.read_csv(data)

    schema = {
        column: str(dtype)
        for column, dtype in df.schema.items()
    }

    return {
        "row_count": df.height,
        "column_count": df.width,
        "schema": json.dumps(schema),
    }


def create_dataset(
    db: Session,
    repository_id: int,
    filename: str,
    data: bytes,
) -> tuple[Dataset, DatasetVersion, bool]:

    # ---------------------------------------------------------
    # 1. Calculate content hash
    # ---------------------------------------------------------
    file_hash = calculate_sha256(data)

    # ---------------------------------------------------------
    # 2. Check whether the actual object already exists
    # ---------------------------------------------------------
    if not storage.object_exists(file_hash):
        storage.upload_bytes(file_hash, data)

    # ---------------------------------------------------------
    # 3. Find the logical dataset
    # ---------------------------------------------------------
    dataset = (
        db.query(Dataset)
        .filter(
            Dataset.repository_id == repository_id,
            Dataset.name == filename,
        )
        .first()
    )

    # ---------------------------------------------------------
    # 4. First upload → create dataset + V1
    # ---------------------------------------------------------
    if dataset is None:

        metadata = get_dataset_metadata(data)

        dataset = Dataset(
            repository_id=repository_id,
            name=filename,
        )

        db.add(dataset)
        db.flush()

        version = DatasetVersion(
            dataset_id=dataset.id,
            version_number=1,
            object_hash=file_hash,
            file_size=len(data),
            row_count=metadata["row_count"],
            column_count=metadata["column_count"],
            schema=metadata["schema"],
        )

        db.add(version)
        db.commit()
        db.refresh(dataset)
        db.refresh(version)

        return dataset, version, True

    # ---------------------------------------------------------
    # 5. Existing dataset → get latest version
    # ---------------------------------------------------------
    latest_version = (
        db.query(DatasetVersion)
        .filter(
            DatasetVersion.dataset_id == dataset.id
        )
        .order_by(
            DatasetVersion.version_number.desc()
        )
        .first()
    )

    if latest_version is None:
        raise ValueError(
            "Dataset exists but has no versions."
        )

    # ---------------------------------------------------------
    # 6. Same content → no new version
    # ---------------------------------------------------------
    if latest_version.object_hash == file_hash:
        return dataset, latest_version, False

    # ---------------------------------------------------------
    # 7. Content changed → create next version
    # ---------------------------------------------------------
    metadata = get_dataset_metadata(data)

    next_version_number = latest_version.version_number + 1

    version = DatasetVersion(
        dataset_id=dataset.id,
        version_number=next_version_number,
        object_hash=file_hash,
        file_size=len(data),
        row_count=metadata["row_count"],
        column_count=metadata["column_count"],
        schema=metadata["schema"],
    )

    db.add(version)
    db.commit()
    db.refresh(version)

    return dataset, version, True

def get_dataset_versions(
    db: Session,
    dataset_id: int,
) -> tuple[Dataset, list[DatasetVersion]] | None:

    dataset = db.get(Dataset, dataset_id)

    if dataset is None:
        return None

    versions = (
        db.query(DatasetVersion)
        .filter(
            DatasetVersion.dataset_id == dataset_id
        )
        .order_by(
            DatasetVersion.version_number.asc()
        )
        .all()
    )

    return dataset, versions

'''
JAI GANESH
JAI SHRIRAM
This function helps retrieve a specific version for dataset

THis uses the app/models/dataset_version.py object to get the specific version 


'''
def get_dataset_version(
    db: Session,
    dataset_id: int,
    version_number: int,
) -> tuple[Dataset, DatasetVersion] | None:

    dataset = db.get(Dataset, dataset_id)

    if dataset is None:
        return None

    version = (
        db.query(DatasetVersion)
        .filter(
            DatasetVersion.dataset_id == dataset_id,
            DatasetVersion.version_number == version_number,
        )
        .first()
    )

    if version is None:
        return None

    return dataset, version

def checkout_dataset_version(
    db: Session,
    dataset_id: int,
    version_number: int,
) -> tuple[Dataset, DatasetVersion] | None:

    dataset = db.get(Dataset, dataset_id)

    if dataset is None:
        return None

    version = (
        db.query(DatasetVersion)
        .filter(
            DatasetVersion.dataset_id == dataset_id,
            DatasetVersion.version_number == version_number,
        )
        .first()
    )

    if version is None:
        return None

    dataset.current_version_id = version.id

    db.commit()
    db.refresh(dataset)
    db.refresh(version)

    return dataset, version