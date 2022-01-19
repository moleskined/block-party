"""empty message

Revision ID: 4d12f6df1078
Revises: cd88d3768949
Create Date: 2022-01-19 13:21:27.215297

"""
from alembic import op
from app import models
import sqlalchemy as sa
from sqlalchemy import Table, MetaData
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date
from datetime import date


# revision identifiers, used by Alembic.
revision = '4d12f6df1078'
down_revision = 'cd88d3768949'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO user (username,role,password_hash) VALUES ('seller', {}, '{}');".format(
        models.Role.SELLER.value, generate_password_hash('pass')))
    op.execute("INSERT INTO user (username,role,password_hash) VALUES ('authority', {}, '{}');".format(
        models.Role.SELLER.value, generate_password_hash('pass')))
    op.execute("INSERT INTO user (username,role,password_hash) VALUES ('buyer', {}, '{}');".format(
        models.Role.SELLER.value, generate_password_hash('pass')))
    op.execute("INSERT INTO user (username,role,password_hash) VALUES ('bank', {}, '{}');".format(
        models.Role.SELLER.value, generate_password_hash('pass')))


def downgrade():
    op.execute("DELETE FROM user WHERE username IN ('seller', 'authority', 'buyer', 'bank');")
