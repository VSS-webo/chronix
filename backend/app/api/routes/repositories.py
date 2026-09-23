print("JAI SHRIRAM")
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.services.repository_service import (
    create_repository,
    get_repositories,
    get_repository,
)


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_repository_endpoint(
    repository_data: RepositoryCreate,
    db: Session = Depends(get_db),
):
    return create_repository(db, repository_data)


@router.get(
    "",
    response_model=list[RepositoryResponse],
)
def list_repositories(
    db: Session = Depends(get_db),
):
    return get_repositories(db)


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
def get_repository_endpoint(
    repository_id: int,
    db: Session = Depends(get_db),
):
    repository = get_repository(db, repository_id)

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    return repository