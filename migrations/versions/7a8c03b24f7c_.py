"""empty message

Revision ID: 7a8c03b24f7c
Revises: e5b059e9dd22
Create Date: 2022-01-21 14:21:03.385717

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash
from app import models


# revision identifiers, used by Alembic.
revision = '7a8c03b24f7c'
down_revision = 'e5b059e9dd22'
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
