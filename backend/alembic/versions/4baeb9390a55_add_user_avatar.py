"""add_user_avatar

Revision ID: 4baeb9390a55
Revises: 8828a8665651
Create Date: 2025-11-29 21:35:32.889991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4baeb9390a55'
down_revision = '8828a8665651'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Добавляем поле avatar в таблицу users
    op.add_column('users', sa.Column('avatar', sa.Text(), nullable=True), schema='config')


def downgrade() -> None:
    # Удаляем поле avatar
    op.drop_column('users', 'avatar', schema='config')
