# print("JAI SHRIRAM")
# from datetime import datetime

# from sqlalchemy import DateTime, ForeignKey, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.core.database import Base


# class Dataset(Base):
#     __tablename__ = "datasets"

#     id: Mapped[int] = mapped_column(primary_key=True)

#     repository_id: Mapped[int] = mapped_column(
#         ForeignKey("repositories.id"),
#         nullable=False,
#         index=True,
#     )

#     name: Mapped[str] = mapped_column(
#         String(255),
#         nullable=False,
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         default=datetime.utcnow,
#         nullable=False,
#     )

#     repository = relationship(
#         "Repository",
#         back_populates="datasets",
#     )
print("JAI SHRIRAM")

# from datetime import datetime

# from sqlalchemy import DateTime, ForeignKey, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.core.database import Base


# class Dataset(Base):
#     __tablename__ = "datasets"

#     id: Mapped[int] = mapped_column(primary_key=True)

#     repository_id: Mapped[int] = mapped_column(
#         ForeignKey("repositories.id"),
#         nullable=False,
#         index=True,
#     )

#     name: Mapped[str] = mapped_column(
#         String(255),
#         nullable=False,
#     )

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         default=datetime.utcnow,
#         nullable=False,
#     )

#     repository = relationship(
#         "Repository",
#         back_populates="datasets",
#     )

#     versions = relationship(
#         "DatasetVersion",
#         back_populates="dataset",
#         cascade="all, delete-orphan",
#     )
print("JAI SHRIRAM")

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    current_version_id: Mapped[int | None] = mapped_column(
        ForeignKey("dataset_versions.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    repository = relationship(
        "Repository",
        back_populates="datasets",
    )

    versions = relationship(
        "DatasetVersion",
        back_populates="dataset",
        foreign_keys="DatasetVersion.dataset_id",
        cascade="all, delete-orphan",
    )

    current_version = relationship(
        "DatasetVersion",
        foreign_keys=[current_version_id],
    )