"""Bind authenticated proposer identity to new Unreviewed Mapping drafts only.

Revision ID: 20261030_04
Revises: 20261030_03

SQLite-only test implementation; NOT a production identity or approval migration.
Existing earlier unattributed drafts remain UNATTRIBUTED (never backfilled).
"""
from alembic import op
import sqlalchemy as sa

revision = "20261030_04"
down_revision = "20261030_03"
branch_labels = None
depends_on = None


def _require_sqlite() -> None:
    if op.get_bind().dialect.name != "sqlite":
        raise RuntimeError(
            "authored Mapping draft migration requires reviewed SQL provider controls; "
            "only SQLite is implemented"
        )


def upgrade() -> None:
    _require_sqlite()
    op.create_table(
        "mapping_draft_authors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("draft_id", sa.Integer(), nullable=False),
        sa.Column("year_id", sa.Integer(), nullable=False),
        sa.Column("issuer", sa.String(length=512), nullable=False),
        sa.Column("subject", sa.String(length=128), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("company_code", sa.String(length=64), nullable=False),
        sa.Column("fiscal_year", sa.Integer(), nullable=False),
        sa.Column("payload_hash", sa.String(length=64), nullable=False),
        sa.Column("author_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.current_timestamp()),
        sa.ForeignKeyConstraint(
            ["draft_id"], ["mapping_review_drafts.id"],
            name="fk_mapping_draft_authors_draft", ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("draft_id", name="uq_mapping_draft_authors_draft"),
        sa.CheckConstraint("role = 'mapping_proposer'",
                           name="ck_mapping_draft_authors_proposer"),
    )
    op.execute(
        """CREATE TRIGGER mapping_draft_authors_no_update
           BEFORE UPDATE ON mapping_draft_authors
           BEGIN SELECT RAISE(ABORT, 'Mapping author evidence is insert-only'); END"""
    )
    op.execute(
        """CREATE TRIGGER mapping_draft_authors_no_delete
           BEFORE DELETE ON mapping_draft_authors
           BEGIN SELECT RAISE(ABORT, 'Mapping author evidence is insert-only'); END"""
    )


def downgrade() -> None:
    _require_sqlite()
    # Destructive; use on disposable CI databases only until a reviewed
    # evidence retention, backup and migration recovery plan exists.
    op.execute("DROP TRIGGER IF EXISTS mapping_draft_authors_no_update")
    op.execute("DROP TRIGGER IF EXISTS mapping_draft_authors_no_delete")
    op.drop_table("mapping_draft_authors")
