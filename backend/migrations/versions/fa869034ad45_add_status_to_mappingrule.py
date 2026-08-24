"""Add status to MappingRule

Revision ID: fa869034ad45
Revises: 20260820_01
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision: str = 'fa869034ad45'
down_revision: Union[str, None] = '20260820_01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('mapping_rules')]
    if 'status' not in columns:
        with op.batch_alter_table('mapping_rules') as batch_op:
            batch_op.add_column(sa.Column('status', sa.String(8), nullable=False, server_default='Draft'))

def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('mapping_rules')]
    if 'status' in columns:
        with op.batch_alter_table('mapping_rules') as batch_op:
            batch_op.drop_column('status')
