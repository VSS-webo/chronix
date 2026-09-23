print("JAI SHRIRAM")

# from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
# from sqlalchemy.orm import Session

# from app.core.database import get_db
# from app.models.repository import Repository
# from app.schemas.dataset import DatasetResponse
# from app.services.dataset_service import create_dataset


# router = APIRouter(
#     prefix="/repositories/{repository_id}/datasets",
#     tags=["Datasets"],
# )


# @router.post(
#     "",
#     response_model=DatasetResponse,
#     status_code=201,
# )
# async def upload_dataset(
#     repository_id: int,
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
# ):
#     # Check that repository exists
#     repository = db.get(Repository, repository_id)

#     if repository is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Repository not found",
#         )

#     # Read uploaded file
#     data = await file.read()

#     if not data:
#         raise HTTPException(
#             status_code=400,
#             detail="Uploaded file is empty",
#         )

#     # Create dataset
#     dataset = create_dataset(
#         db=db,
#         repository_id=repository_id,
#         filename=file.filename,
#         data=data,
#     )

#     return dataset
print("JAI SHRIRAM")

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.repository import Repository
from app.services.dataset_service import create_dataset
from fastapi.responses import Response
from app.storage.minio_storage import MinIOStorage

storage=MinIOStorage()


from app.schemas.dataset import (
    DatasetVersionHistoryResponse,
    DatasetVersionResponse,
)

from app.services.dataset_service import (
    create_dataset,
    get_dataset_versions,
    get_dataset_version,
    checkout_dataset_version
)


router = APIRouter(
    prefix="/repositories/{repository_id}/datasets",
    tags=["Datasets"],
)


@router.post("")
async def upload_dataset(
    repository_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # ---------------------------------------------------------
    # Check repository
    # ---------------------------------------------------------
    repository = db.get(Repository, repository_id)

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    # ---------------------------------------------------------
    # Read uploaded file
    # ---------------------------------------------------------
    data = await file.read()

    if not data:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty",
        )

    # ---------------------------------------------------------
    # Create dataset/version
    # ---------------------------------------------------------
    dataset, version, created = create_dataset(
        db=db,
        repository_id=repository_id,
        filename=file.filename,
        data=data,
    )

    # ---------------------------------------------------------
    # Existing content
    # ---------------------------------------------------------
    if not created:
        return {
            "message": "Dataset unchanged. Already latest version. No new version created.",
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "version": version.version_number,
            "object_hash": version.object_hash,
        }

    # ---------------------------------------------------------
    # New version
    # ---------------------------------------------------------
    return {
        "message": f"Dataset uploaded successfully. Version {version.version_number} created.",
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        "version": version.version_number,
        "object_hash": version.object_hash,
        "file_size": version.file_size,
        "row_count": version.row_count,
        "column_count": version.column_count,
        "schema": version.schema,
    }

@router.get(
    "/{dataset_id}/versions",
    response_model=DatasetVersionHistoryResponse,
)
def get_dataset_version_history(
    repository_id: int,
    dataset_id: int,
    db: Session = Depends(get_db),
):
    result = get_dataset_versions(
        db=db,
        dataset_id=dataset_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    dataset, versions = result

    # Make sure the dataset actually belongs
    # to the repository in the URL.
    if dataset.repository_id != repository_id:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found in this repository",
        )

    return {
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        "versions": versions,
    }

@router.get(
    "/{dataset_id}/versions/{version_number}",
    response_model=DatasetVersionResponse,
)
def get_specific_dataset_version(
    repository_id: int,
    dataset_id: int,
    version_number: int,
    db: Session = Depends(get_db),
):
    result = get_dataset_version(
        db=db,
        dataset_id=dataset_id,
        version_number=version_number,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset version not found",
        )

    dataset, version = result

    # Make sure the dataset belongs to this repository
    if dataset.repository_id != repository_id:
        raise HTTPException(
            status_code=404,
            detail="Dataset version not found",
        )

    return version

@router.get(
    "/{dataset_id}/versions/{version_number}/download"
)
def download_dataset_version(
    repository_id: int,
    dataset_id: int,
    version_number: int,
    db: Session = Depends(get_db),
):
    result = get_dataset_version(
        db=db,
        dataset_id=dataset_id,
        version_number=version_number,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset version not found",
        )

    dataset, version = result

    # Make sure dataset belongs to repository
    if dataset.repository_id != repository_id:
        raise HTTPException(
            status_code=404,
            detail="Dataset version not found",
        )

    try:
        data = storage.download_bytes(
            version.object_hash
        )
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Dataset object not found in storage",
        )

    return Response(
        content=data,
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{dataset.name}"'
            )
        },
    )

@router.post(
    "/{dataset_id}/checkout/{version_number}"
)
def checkout_dataset(
    repository_id: int,
    dataset_id: int,
    version_number: int,
    db: Session = Depends(get_db),
):
    result = checkout_dataset_version(
        db=db,
        dataset_id=dataset_id,
        version_number=version_number,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset version not found",
        )

    dataset, version = result

    if dataset.repository_id != repository_id:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found in this repository",
        )

    return {
        "message": f"Dataset checked out to version {version.version_number}.",
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        "current_version": version.version_number,
        "current_version_id": version.id,
        "object_hash": version.object_hash,
    }