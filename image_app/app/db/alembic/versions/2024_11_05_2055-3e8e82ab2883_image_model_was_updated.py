"""Image model was updated

Revision ID: 3e8e82ab2883
Revises: 2da1ee1e8fa3
Create Date: 2024-11-05 20:55:52.062115

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e8e82ab2883"
down_revision: Union[str, None] = "2da1ee1e8fa3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "images",
        "size",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        type_=sa.Integer(),
        existing_nullable=False,
    )
    op.drop_constraint("images_uploaded_at_key", "images", type_="unique")


def downgrade() -> None:
    op.create_unique_constraint("images_uploaded_at_key", "images", ["uploaded_at"])
    op.alter_column(
        "images",
        "size",
        existing_type=sa.Integer(),
        type_=sa.DOUBLE_PRECISION(precision=53),
        existing_nullable=False,
    )
