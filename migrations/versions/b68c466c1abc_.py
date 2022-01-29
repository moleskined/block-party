"""empty message

Revision ID: b68c466c1abc
Revises: 45c6ea2e338c
Create Date: 2022-01-28 17:27:06.127229

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash
from app import models


# revision identifiers, used by Alembic.
revision = 'b68c466c1abc'
down_revision = '45c6ea2e338c'
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
    op.execute(
        "DELETE FROM user WHERE username IN ('seller', 'authority', 'buyer', 'bank');")
