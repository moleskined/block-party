from datetime import datetime
import hashlib as hasher
from enum import Enum
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64


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
    timestamp = db.Column(db.DateTime, nullable=False)
    previous_hash = db.Column(db.String(50), index=True)
    property_address = db.Column(db.String(256), nullable=False)
    seller_details = db.Column(db.String(256), nullable=False)
    building_design = db.Column(db.LargeBinary, nullable=False)
    seller_licence_number = db.Column(db.String(23), nullable=False)
    hash = db.Column(db.String(50), primary_key=True)

    def __init__(self, timestamp: datetime, previous_hash: str, property_address: str,
                 seller_details: str, building_design: bytes, seller_licence_number: str) -> None:
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.property_address = property_address
        self.seller_details = seller_details
        self.building_design = building_design
        self.seller_licence_number = seller_licence_number
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        base64_bytes = base64.b64encode(self.building_design)
        base64_message = base64_bytes.decode('utf-8')
        txt = str(self.timestamp) + str(self.previous_hash) + str(self.property_address) + str(
            self.seller_details) + str(self.building_design) + base64_message + str(self.seller_licence_number)
        sha.update(txt.encode('utf-8'))
        return sha.hexdigest()


class AuthorisationBlock(db.Model):
    timestamp = db.Column(db.DateTime, nullable=False)
    previous_hash = db.Column(db.String(50), index=True)
    property_address = db.Column(db.String(256), nullable=False)
    approval_status = db.Column(db.SmallInteger, nullable=False)
    hash = db.Column(db.String(50), primary_key=True)

    def __init__(self, timestamp: datetime, previous_hash: str, approval_status: bool, property_address: str) -> None:
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.property_address = property_address
        self.approval_status = approval_status
        self.hash = self.hash_block()

    def hash_block(self) -> str:
        sha = hasher.sha256()
        txt = str(self.timestamp) + str(self.previous_hash) + \
            str(self.property_address) + str(1 if self.approval_status else 0)
        sha.update(txt.encode('utf-8'))
        return sha.hexdigest()


class Role(Enum):
    NONE = -1
    SELLER = 1
    AUTHORITY = 2
    BUYER = 3
    BANK = 4


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
