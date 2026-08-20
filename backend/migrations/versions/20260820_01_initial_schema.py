"""Initial Phase 2A schema.

Revision ID: 20260820_01
"""
from alembic import op

from aram_backend.database import Base
from aram_backend import models  # noqa: F401

revision = "20260820_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)

