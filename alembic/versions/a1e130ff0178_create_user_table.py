"""create user table

Revision ID: a1e130ff0178
Revises: 
Create Date: 2025-04-21 18:07:24.241884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1e130ff0178'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
                    sa.Column("id", sa.Integer, primary_key=True, index=True),
                    sa.Column("email", sa.String(50), index=True),
                    sa.Column("first_name", sa.String(50)),
                    sa.Column("last_name", sa.String(50)))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
