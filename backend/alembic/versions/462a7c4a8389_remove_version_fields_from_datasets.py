"""remove version fields from datasets

Revision ID: 462a7c4a8389
Revises: 9a5fd58ff858
Create Date: 2026-09-21 08:33:36.768801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '462a7c4a8389'
down_revision: Union[str, Sequence[str], None] = '9a5fd58ff858'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("datasets", "object_hash")
    op.drop_column("datasets", "file_size")
    op.drop_column("datasets", "row_count")
    op.drop_column("datasets", "column_count")
    op.drop_column("datasets", "schema")


def downgrade() -> None:
    op.add_column(
        "datasets",
        sa.Column("schema", sa.Text(), nullable=True),
    )
    op.add_column(
        "datasets",
        sa.Column("column_count", sa.Integer(), nullable=True),
    )
    op.add_column(
        "datasets",
        sa.Column("row_count", sa.Integer(), nullable=True),
    )
    op.add_column(
        "datasets",
        sa.Column("file_size", sa.Integer(), nullable=True),
    )
    op.add_column(
        "datasets",
        sa.Column("object_hash", sa.String(length=64), nullable=True),
    )