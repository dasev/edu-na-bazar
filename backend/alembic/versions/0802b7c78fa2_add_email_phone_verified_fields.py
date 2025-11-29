"""add_email_phone_verified_fields

Revision ID: 0802b7c78fa2
Revises: 4baeb9390a55
Create Date: 2025-11-29 21:51:44.552423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0802b7c78fa2'
down_revision = '4baeb9390a55'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Добавляем поля is_email_verified и is_phone_verified
    op.add_column('users', sa.Column('is_email_verified', sa.Boolean(), server_default='false', nullable=False), schema='config')
    op.add_column('users', sa.Column('is_phone_verified', sa.Boolean(), server_default='false', nullable=False), schema='config')


def downgrade() -> None:
    # Удаляем поля
    op.drop_column('users', 'is_phone_verified', schema='config')
    op.drop_column('users', 'is_email_verified', schema='config')
