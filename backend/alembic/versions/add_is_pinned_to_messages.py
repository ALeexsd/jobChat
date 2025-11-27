"""add is_pinned to messages

Revision ID: f7b8c9d0e1f2
Revises: d4f8a2b3c1e5
Create Date: 2025-11-23 20:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7b8c9d0e1f2'
down_revision = '1ee6e4c1784e'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_pinned column to messages table
    op.add_column('messages', sa.Column('is_pinned', sa.Boolean(), nullable=False, server_default='false'))


def downgrade():
    # Remove is_pinned column from messages table
    op.drop_column('messages', 'is_pinned')
