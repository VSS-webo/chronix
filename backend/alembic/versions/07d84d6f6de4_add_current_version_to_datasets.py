"""add current version to datasets

Revision ID: 07d84d6f6de4
Revises: 462a7c4a8389
Create Date: 2026-09-21 09:57:36.551640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07d84d6f6de4'
down_revision: Union[str, Sequence[str], None] = '462a7c4a8389'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "datasets",
        sa.Column(
            "current_version_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_datasets_current_version",
        "datasets", 
        "dataset_versions",
        ["current_version_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_datasets_current_version",
        "datasets",
        type_="foreignkey",
    )

    op.drop_column(
        "datasets",
        "current_version_id",
    )
