"""add timezone to timestamps

Revision ID: 02ef4b71cd5c
Revises: 1470926fa825
Create Date: 2022-04-28 09:30:50.111271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "02ef4b71cd5c"
down_revision = "1470926fa825"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name="response_data",
        column_name="created_timestamp",
        type_=sa.TIMESTAMP(timezone=True),
    )
    op.alter_column(
        table_name="test_run",
        column_name="created_timestamp",
        type_=sa.TIMESTAMP(timezone=True),
    )


def downgrade():
    op.alter_column(
        table_name="response_data",
        column_name="created_timestamp",
        type_=sa.TIMESTAMP(),
    )
    op.alter_column(
        table_name="test_run", column_name="created_timestamp", type_=sa.TIMESTAMP()
    )
