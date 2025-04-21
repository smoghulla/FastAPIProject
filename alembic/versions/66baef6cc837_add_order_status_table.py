"""add order status table

Revision ID: 66baef6cc837
Revises: 2706a0f003a5
Create Date: 2025-04-21 18:35:30.024455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision: str = '66baef6cc837'
down_revision: Union[str, None] = '2706a0f003a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("order_statuses",
                    sa.Column("id", sa.Integer(), primary_key=True, index=True),
                    sa.Column("order_id", sa.Integer(), ForeignKey("orders.id")),
                    sa.Column("order_status", sa.String(20)),
                    sa.Column("status_update_time", sa.DateTime(), default=datetime.now))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("order_statuses")
