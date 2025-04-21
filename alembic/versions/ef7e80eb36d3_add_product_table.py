"""add product table

Revision ID: ef7e80eb36d3
Revises: a1e130ff0178
Create Date: 2025-04-21 18:31:03.074302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef7e80eb36d3'
down_revision: Union[str, None] = 'a1e130ff0178'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("products",
                    sa.Column("id", sa.Integer, primary_key=True, index=True),
                    sa.Column("product_name", sa.String(50)),
                    sa.Column("cost", sa.DECIMAL(10,2)),
                    sa.Column("description", sa.String(255)))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("products")
