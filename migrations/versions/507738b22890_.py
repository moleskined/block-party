"""empty message

Revision ID: 507738b22890
Revises: a865841c06bd
Create Date: 2022-01-22 14:07:30.203269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '507738b22890'
down_revision = 'a865841c06bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank_approval',
    sa.Column('hash', sa.String(length=50), nullable=False),
    sa.Column('previous_hash', sa.String(length=50), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('approval_status', sa.SmallInteger(), nullable=False),
    sa.Column('full_name', sa.String(length=256), nullable=False),
    sa.Column('current_address', sa.String(length=256), nullable=False),
    sa.Column('contact_number', sa.String(length=50), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_index(op.f('ix_bank_approval_previous_hash'), 'bank_approval', ['previous_hash'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bank_approval_previous_hash'), table_name='bank_approval')
    op.drop_table('bank_approval')
    # ### end Alembic commands ###
