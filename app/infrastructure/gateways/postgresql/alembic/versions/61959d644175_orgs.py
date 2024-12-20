"""orgs

Revision ID: 61959d644175
Revises:
Create Date: 2024-11-15 21:46:24.141980

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "61959d644175"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "orgs",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("logo", sa.String(), nullable=False),
        sa.Column("foundation_year", sa.Integer(), nullable=False),
        sa.Column("scope", sa.String(), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orgs")),
        sa.UniqueConstraint("email", name=op.f("uq_orgs_email")),
        sa.UniqueConstraint("id", name=op.f("uq_orgs_id"))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("orgs")
    # ### end Alembic commands ###
