"""initial migration

Revision ID: 2da1ee1e8fa3
Revises: 
Create Date: 2024-11-03 04:48:40.768730

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2da1ee1e8fa3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "images",
        sa.Column("file_name", sa.String(), nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column(
            "uploaded_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("resolution", sa.String(), nullable=False),
        sa.Column("size", sa.Float(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("file_name"),
        sa.UniqueConstraint("file_path"),
        sa.UniqueConstraint("uploaded_at"),
    )


def downgrade() -> None:
    op.drop_table("images")
