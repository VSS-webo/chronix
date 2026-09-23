print("JAI SHRIRAM")

from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate


def create_repository(
    db: Session,
    repository_data: RepositoryCreate,
) -> Repository:

    repository = Repository(
        name=repository_data.name
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository


def get_repositories(db: Session) -> list[Repository]:
    return db.query(Repository).all()


def get_repository(
    db: Session,
    repository_id: int,
) -> Repository | None:

    return db.get(Repository, repository_id)