"""add users

Revision ID: 919a33565eef
Revises: a66fe45b82df
Create Date: 2025-10-12 20:31:14.405844

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "919a33565eef"
down_revision: Union[str, Sequence[str], None] = "a66fe45b82df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
