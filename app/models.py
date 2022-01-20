from enum import Enum
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,
                         unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PermitApplication(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    previous_hash = db.Column(db.String(512), index=True)
    hash = db.Column(db.String(512), unique=True, nullable=False, index=True)
    property_address = db.Column(db.String(256), nullable=False)
    building_design = db.Column(db.LargeBinary, nullable=False)
    permit_application_id = db.Column(db.String(23), nullable=False)
    seller_details = db.Column(db.String(256), nullable=False)
    seller_licence_number = db.Column(db.String(23), nullable=False)


class Role(Enum):
    NONE = -1
    SELLER = 1
    AUTHORITY = 2
    BUYER = 3
    BANK = 4


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
