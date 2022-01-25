"""empty message

Revision ID: fffc78294b86
Revises: 79e7695f9765
Create Date: 2022-01-21 18:24:37.209171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fffc78294b86'
down_revision = '79e7695f9765'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authorisation_blocks',
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('previous_hash', sa.String(length=50), nullable=True),
    sa.Column('property_address', sa.String(length=256), nullable=False),
    sa.Column('approval_status', sa.SmallInteger(), nullable=False),
    sa.Column('hash', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_index(op.f('ix_authorisation_blocks_previous_hash'), 'authorisation_blocks', ['previous_hash'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_authorisation_blocks_previous_hash'), table_name='authorisation_blocks')
    op.drop_table('authorisation_blocks')
    # ### end Alembic commands ###
