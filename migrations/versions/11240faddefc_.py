"""empty message

Revision ID: 11240faddefc
Revises: 91caa1348ae6
Create Date: 2022-01-21 08:59:09.486481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11240faddefc'
down_revision = '91caa1348ae6'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "INSERT INTO permit_application VALUES (0, '2022-01-01', null, 'GENESIS', '', '', '', '', '')")


def downgrade():
    pass
