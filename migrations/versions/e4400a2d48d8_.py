"""empty message

Revision ID: e4400a2d48d8
Revises: 40d1da15458a
Create Date: 2022-01-25 23:25:28.333270

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash
from app import models


# revision identifiers, used by Alembic.
revision = 'e4400a2d48d8'
down_revision = '40d1da15458a'
branch_labels = None
depends_on = None


def upgrade():
    # Insert default users
    op.execute("INSERT INTO user (username,role,password_hash) VALUES ('seller', {}, '{}');".format(
        models.Role.SELLER.value, generate_password_hash('pass')))
    op.execute("INSERT INTO user (username,role,password_hash) VALUES ('authority', {}, '{}');".format(
        models.Role.AUTHORITY.value, generate_password_hash('pass')))
    op.execute("INSERT INTO user (username,role,password_hash) VALUES ('buyer', {}, '{}');".format(
        models.Role.BUYER.value, generate_password_hash('pass')))
    op.execute("INSERT INTO user (username,role,password_hash) VALUES ('bank', {}, '{}');".format(
        models.Role.BANK.value, generate_password_hash('pass')))


def downgrade():
    op.execute("DELETE FROM user WHERE username IN ('seller', 'authority', 'buyer', 'bank');")
