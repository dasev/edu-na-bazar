"""Add product views tracking

Revision ID: add_product_views
Revises: 0802b7c78fa2
Create Date: 2025-11-30 01:53:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_product_views'
down_revision = '0802b7c78fa2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Создаем таблицу product_views
    op.create_table(
        'product_views',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('product_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('session_id', sa.String(255), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['market.products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['config.users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        schema='market'
    )
    
    # Создаем индексы
    op.create_index('ix_market_product_views_product_id', 'product_views', ['product_id'], schema='market')
    op.create_index('ix_market_product_views_user_id', 'product_views', ['user_id'], schema='market')
    op.create_index('ix_market_product_views_session_id', 'product_views', ['session_id'], schema='market')
    op.create_index('ix_market_product_views_created_at', 'product_views', ['created_at'], schema='market')


def downgrade() -> None:
    op.drop_index('ix_market_product_views_created_at', 'product_views', schema='market')
    op.drop_index('ix_market_product_views_session_id', 'product_views', schema='market')
    op.drop_index('ix_market_product_views_user_id', 'product_views', schema='market')
    op.drop_index('ix_market_product_views_product_id', 'product_views', schema='market')
    op.drop_table('product_views', schema='market')
