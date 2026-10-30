"""SQLite-only system staging audit events; not human approval or WORM evidence.

Revision ID: 20261030_03
Revises: 20261030_02
"""
from alembic import op
import sqlalchemy as sa

revision = "20261030_03"
down_revision = "20261030_02"
branch_labels = None
depends_on = None


def _require_sqlite() -> None:
    # Other providers need separately reviewed trigger/privilege implementations;
    # silently creating a mutable "audit" table would be misleading.
    if op.get_bind().dialect.name != "sqlite":
        raise RuntimeError(
            "Mapping staging audit migration requires reviewed provider-specific "
            "insert-only protections; only SQLite is implemented"
        )


def upgrade() -> None:
    _require_sqlite()
    # PR #53 may already contain real Unreviewed drafts. Creating an empty
    # event table would orphan their evidence and make future reads fail.
    # Do not invent historical system events: require a separately approved
    # documented backfill/recovery plan before upgrading such a database.
    if op.get_bind().execute(
        sa.text("SELECT 1 FROM mapping_review_drafts LIMIT 1")
    ).first() is not None:
        raise RuntimeError(
            "existing Unreviewed drafts require reviewed audit backfill "
            "or recovery before this migration"
        )
    op.create_table(
        "mapping_draft_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("draft_id", sa.Integer(), nullable=False),
        sa.Column("year_id", sa.Integer(), nullable=False),
        sa.Column(
            "event_type", sa.String(length=32), nullable=False,
            server_default="DraftStaged",
        ),
        sa.Column("payload_hash", sa.String(length=64), nullable=False),
        sa.Column("event_hash", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.ForeignKeyConstraint(
            ["draft_id"], ["mapping_review_drafts.id"],
            name="fk_mapping_draft_events_draft", ondelete="RESTRICT",
        ),
        sa.UniqueConstraint("draft_id", name="uq_mapping_draft_events_draft"),
        sa.CheckConstraint(
            "event_type = 'DraftStaged'",
            name="ck_mapping_draft_events_staging_only",
        ),
    )
    op.execute(
        """CREATE TRIGGER mapping_draft_events_no_update
           BEFORE UPDATE ON mapping_draft_events
           BEGIN SELECT RAISE(ABORT, 'Mapping staging event is insert-only'); END"""
    )
    op.execute(
        """CREATE TRIGGER mapping_draft_events_no_delete
           BEFORE DELETE ON mapping_draft_events
           BEGIN SELECT RAISE(ABORT, 'Mapping staging event is insert-only'); END"""
    )


def downgrade() -> None:
    _require_sqlite()
    # Downgrade is destructive and needs an explicit reviewed backup/recovery
    # decision before use against ANY real dataset.
    op.execute("DROP TRIGGER IF EXISTS mapping_draft_events_no_update")
    op.execute("DROP TRIGGER IF EXISTS mapping_draft_events_no_delete")
    op.drop_table("mapping_draft_events")
