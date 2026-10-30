"""Store Mapping drafts only; no approval workflow or MappingRule write.

Revision ID: 20261030_02
Revises: 20260820_01
"""
from alembic import op
import sqlalchemy as sa

revision = "20261030_02"
down_revision = "20260820_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Separate from Base.metadata: the baseline initial revision calls
    # Base.metadata.create_all(). Explicit DDL prevents duplicate creation.
    op.create_table(
        "mapping_review_drafts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("year_id", sa.Integer(), nullable=False),
        sa.Column("request_key", sa.String(length=64), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column("payload_hash", sa.String(length=64), nullable=False),
        sa.Column(
            "state", sa.String(length=16), nullable=False,
            server_default="Unreviewed",
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.ForeignKeyConstraint(["year_id"], ["fiscal_years.id"], ondelete="RESTRICT",
                                name="fk_mapping_review_drafts_year_id_fiscal_years"),
        sa.UniqueConstraint("year_id", "request_key", name="uq_mapping_review_drafts_year_request"),
        sa.CheckConstraint("state = 'Unreviewed'",
                           name="ck_mapping_review_drafts_unreviewed_only"),
    )


def downgrade() -> None:
    op.drop_table("mapping_review_drafts")
