"""add order table

Revision ID: 2706a0f003a5
Revises: ef7e80eb36d3
Create Date: 2025-04-21 18:32:38.134070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision: str = '2706a0f003a5'
down_revision: Union[str, None] = 'ef7e80eb36d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("orders",
                    sa.Column("id", sa.Integer, primary_key=True, index=True),
                    sa.Column("product_id", sa.Integer,ForeignKey("products.id")),
                    sa.Column("cost", sa.DECIMAL(10,2)),
                    sa.Column("quantity",sa.Integer),
                    sa.Column("total_amount", sa.DECIMAL(10,2)),
                    sa.Column("user_id", sa.Integer),ForeignKey("users.id"))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("orders")
