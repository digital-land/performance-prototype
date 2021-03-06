"""Move assertion outcome to separate table

Revision ID: c6e76ab376a8
Revises: 02ef4b71cd5c
Create Date: 2022-04-28 11:15:25.553880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c6e76ab376a8"
down_revision = "02ef4b71cd5c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "assertion",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("expected", sa.Text(), nullable=False),
        sa.Column("actual", sa.Text(), nullable=True),
        sa.Column("match", sa.BOOLEAN(), nullable=True),
        sa.Column("test_result_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["test_result_id"],
            ["result.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_column("result", "match")
    op.drop_column("result", "expected")
    op.drop_column("result", "actual")
    op.drop_column("result", "path")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "result", sa.Column("path", sa.TEXT(), autoincrement=False, nullable=False)
    )
    op.add_column(
        "result", sa.Column("actual", sa.TEXT(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "result", sa.Column("expected", sa.TEXT(), autoincrement=False, nullable=False)
    )
    op.add_column(
        "result", sa.Column("match", sa.BOOLEAN(), autoincrement=False, nullable=True)
    )
    op.drop_table("assertion")
    # ### end Alembic commands ###
