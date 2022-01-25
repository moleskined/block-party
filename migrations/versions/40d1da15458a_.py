"""empty message

Revision ID: 40d1da15458a
Revises: 
Create Date: 2022-01-25 23:24:41.612018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40d1da15458a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authorisation_block',
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('previous_hash', sa.String(length=50), nullable=True),
    sa.Column('property_address', sa.String(length=256), nullable=False),
    sa.Column('approval_status', sa.SmallInteger(), nullable=False),
    sa.Column('hash', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_index(op.f('ix_authorisation_block_previous_hash'), 'authorisation_block', ['previous_hash'], unique=False)
    op.create_table('bank_approval',
    sa.Column('hash', sa.String(length=50), nullable=False),
    sa.Column('previous_hash', sa.String(length=50), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('approval_status', sa.SmallInteger(), nullable=False),
    sa.Column('full_name', sa.String(length=256), nullable=False),
    sa.Column('current_address', sa.String(length=256), nullable=False),
    sa.Column('contact_number', sa.String(length=50), nullable=False),
    sa.Column('dob', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_index(op.f('ix_bank_approval_previous_hash'), 'bank_approval', ['previous_hash'], unique=False)
    op.create_table('block',
    sa.Column('hash', sa.String(length=50), nullable=False),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('previous_hash', sa.String(length=50), nullable=True),
    sa.Column('data', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_index(op.f('ix_block_previous_hash'), 'block', ['previous_hash'], unique=False)
    op.create_table('buyer_block',
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('previous_hash', sa.String(length=50), nullable=True),
    sa.Column('full_name', sa.String(length=256), nullable=False),
    sa.Column('dob', sa.String(length=10), nullable=False),
    sa.Column('current_address', sa.String(length=256), nullable=False),
    sa.Column('contact_number', sa.String(length=50), nullable=False),
    sa.Column('employer_name', sa.String(length=256), nullable=False),
    sa.Column('annual_income', sa.Numeric(), nullable=False),
    sa.Column('property_address', sa.String(length=256), nullable=False),
    sa.Column('loan_amount', sa.Numeric(), nullable=False),
    sa.Column('hash', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_index(op.f('ix_buyer_block_previous_hash'), 'buyer_block', ['previous_hash'], unique=False)
    op.create_table('permit_application',
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('previous_hash', sa.String(length=50), nullable=True),
    sa.Column('property_address', sa.String(length=256), nullable=False),
    sa.Column('seller_details', sa.String(length=256), nullable=False),
    sa.Column('building_design', sa.LargeBinary(), nullable=False),
    sa.Column('seller_licence_number', sa.String(length=23), nullable=False),
    sa.Column('hash', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_index(op.f('ix_permit_application_previous_hash'), 'permit_application', ['previous_hash'], unique=False)
    op.create_table('sale_finalisation_block',
    sa.Column('hash', sa.String(length=50), nullable=False),
    sa.Column('previous_hash', sa.String(length=50), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('approved', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_index(op.f('ix_sale_finalisation_block_previous_hash'), 'sale_finalisation_block', ['previous_hash'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_sale_finalisation_block_previous_hash'), table_name='sale_finalisation_block')
    op.drop_table('sale_finalisation_block')
    op.drop_index(op.f('ix_permit_application_previous_hash'), table_name='permit_application')
    op.drop_table('permit_application')
    op.drop_index(op.f('ix_buyer_block_previous_hash'), table_name='buyer_block')
    op.drop_table('buyer_block')
    op.drop_index(op.f('ix_block_previous_hash'), table_name='block')
    op.drop_table('block')
    op.drop_index(op.f('ix_bank_approval_previous_hash'), table_name='bank_approval')
    op.drop_table('bank_approval')
    op.drop_index(op.f('ix_authorisation_block_previous_hash'), table_name='authorisation_block')
    op.drop_table('authorisation_block')
    # ### end Alembic commands ###