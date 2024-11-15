"""applies

Revision ID: 892557aadcc9
Revises: 61959d644175
Create Date: 2024-11-15 20:47:05.108599

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "892557aadcc9"
down_revision: Union[str, None] = "61959d644175"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "applies",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("org_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("experience", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_applies")),
        sa.UniqueConstraint("id", name=op.f("uq_applies_id")),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["orgs.id"],
            name=op.f("fk_applies_org_id_orgs"),
            ondelete="CASCADE"
        ),
    )
    op.create_table(
        "user_interests",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("apply_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("interest", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["apply_id"],
            ["applies.id"],
            name=op.f("fk_user_interests_apply_id_applies"),
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_interests")),
        sa.UniqueConstraint("id", name=op.f("uq_user_interests_id"))
    )
    op.create_table(
        "user_skills",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("apply_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("skill", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["apply_id"],
            ["applies.id"],
            name=op.f("fk_user_skills_apply_id_applies"),
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_skills")),
        sa.UniqueConstraint("id", name=op.f("uq_user_skills_id"))
    )

    # ### end Alembic commands ###

    def downgrade() -> None:
        # ### commands auto generated by Alembic - please adjust! ###
        op.drop_table("user_skills")
        op.drop_table("user_interests")
        op.drop_table("applies")
        # ### end Alembic commands ###