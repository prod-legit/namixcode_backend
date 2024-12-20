"""jobs

Revision ID: f9042b7bb3de
Revises: dae2429e98fb
Create Date: 2024-11-16 22:10:15.713137

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f9042b7bb3de"
down_revision: Union[str, None] = "dae2429e98fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "jobs",
        sa.Column("org_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("pay", sa.String(), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.ForeignKeyConstraint(["org_id"], ["orgs.id"], name=op.f("fk_jobs_org_id_orgs"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_jobs")),
        sa.UniqueConstraint("id", name=op.f("uq_jobs_id"))
    )
    op.add_column("applies", sa.Column("job_id", sa.UUID(as_uuid=False), nullable=False))
    op.create_unique_constraint(op.f("uq_applies_id"), "applies", ["id"])
    op.drop_constraint("fk_applies_org_id_orgs", "applies", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_applies_job_id_jobs"),
        "applies",
        "jobs",
        ["job_id"],
        ["id"],
        ondelete="CASCADE"
    )
    op.drop_column("applies", "org_id")
    op.add_column("employees", sa.Column("job_id", sa.UUID(as_uuid=False), nullable=False))
    op.create_unique_constraint(op.f("uq_employees_id"), "employees", ["id"])
    op.drop_constraint("fk_employees_org_id_orgs", "employees", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_employees_job_id_jobs"),
        "employees",
        "jobs",
        ["job_id"],
        ["id"],
        ondelete="CASCADE"
    )
    op.drop_column("employees", "org_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("employees", sa.Column("org_id", sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f("fk_employees_job_id_jobs"), "employees", type_="foreignkey")
    op.create_foreign_key(
        "fk_employees_org_id_orgs",
        "employees",
        "orgs",
        ["org_id"],
        ["id"],
        ondelete="CASCADE"
    )
    op.drop_constraint(op.f("uq_employees_id"), "employees", type_="unique")
    op.drop_column("employees", "job_id")
    op.add_column("applies", sa.Column("org_id", sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(op.f("fk_applies_job_id_jobs"), "applies", type_="foreignkey")
    op.create_foreign_key(
        "fk_applies_org_id_orgs",
        "applies",
        "orgs",
        ["org_id"],
        ["id"],
        ondelete="CASCADE"
    )
    op.drop_constraint(op.f("uq_applies_id"), "applies", type_="unique")
    op.drop_column("applies", "job_id")
    op.drop_table("jobs")
    # ### end Alembic commands ###
