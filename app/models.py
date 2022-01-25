import base64
import hashlib as hasher
from datetime import date, datetime
from enum import Enum
import json
from unicodedata import decimal
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


MAX_DATA_DISPLAY_LENGTH = 400


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


class Block(db.Model):
    hash = db.Column(db.String(50), primary_key=True)
    index = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    previous_hash = db.Column(db.String(50), index=True)
    data = db.Column(db.Text)
    previous_instance = None
    is_head = False

    def __init__(self, timestamp: datetime, index: int, previous_hash: str, data: str) -> None:
        super().__init__()
        self.previous_instance = None
        self.is_head = False
        self.timestamp = timestamp
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.hash = self.hash_block()

    def get_hash_text(self):
        return "{}{}{}{}".format(
            self.timestamp, self.index, self.previous_hash, self.data)

    def hash_block(self):
        sha = hasher.sha256()
        txt = self.get_hash_text()
        sha.update(txt.encode('utf-8'))
        return sha.hexdigest()

    def set_prev(self, block):
        self.previous_instance = block

    def get_prev(self):
        return self.previous_instance

    def set_is_head(self, is_head):
        self.is_head = is_head

    def get_is_head(self):
        return self.is_head

    def __repr__(self) -> str:
        return self.hash

    def __str__(self) -> str:
        str = ""
        str += "index: {0}\n".format(self.index)
        str += "hash: {0}\n".format(self.hash)
        str += "previous_hash: {0}\n".format(self.previous_hash)
        str += "data:\n"

        data_json: dict = json.loads(self.data)
        key = list(data_json.keys())[0]
        str += "\t{0}:".format(key)
        inner_data: dict = data_json[key]
        for key in inner_data:
            value = "{}".format(inner_data[key])[:MAX_DATA_DISPLAY_LENGTH]
            str += "\n\t\t{}: {}".format(key, value)
        return str


class BlockChain():
    def __init__(self, head: Block) -> None:
        self.head = head
        self.denormalised = self.denormalise()
        self.index = self.index_data()

    def flatten(self) -> str:
        return self.denormalised

    def get_head(self) -> Block:
        return self.head

    def index_data(self):
        index = {}
        keys = {}
        nxt = self.head
        while nxt is not None:
            keys[nxt.hash] = nxt
            data = json.loads(nxt.data)
            key = list(data.keys())[0]
            index[key] = data[key]
            nxt = nxt.get_prev()
        index['__by_hash'] = keys
        return index

    def denormalise(self):
        denormalised_block_list = []

        block = self.get_head()

        if block is not None:
            data = json.loads(block.data)
            if "SaleFinalisationTransaction" in data:
                result = {'__type': 'SaleFinalisationBlock'}
                result['timestamp'] = block.timestamp.isoformat()
                result['previous_hash'] = block.previous_hash
                result['hash'] = block.hash
                result['index'] = block.index
                d = data["SaleFinalisationTransaction"]
                result['approved'] = d['approved']
                denormalised_block_list.append(result)
                block = block.get_prev()

        if block is not None:
            data = json.loads(block.data)
            if "BankApprovalTransaction" in data:
                result = {'__type': 'BankApproval'}
                result['timestamp'] = block.timestamp.isoformat()
                result['previous_hash'] = block.previous_hash
                result['hash'] = block.hash
                result['index'] = block.index
                d = data["BankApprovalTransaction"]
                result['approval_status'] = d["approval_status"]
                result['full_name'] = d["full_name"]
                result['current_address'] = d["current_address"]
                result['contact_number'] = d["contact_number"]
                result['dob'] = d["dob"]
                denormalised_block_list.append(result)
                block = block.get_prev()

        if block is not None:
            data = json.loads(block.data)
            if "BuyerTransaction" in data:
                result = {'__type': 'BuyerBlock'}
                result['timestamp'] = block.timestamp.isoformat()
                result['previous_hash'] = block.previous_hash
                result['hash'] = block.hash
                result['index'] = block.index
                d = data["BuyerTransaction"]
                result['full_name'] = d["full_name"]
                result['dob'] = d["dob"]
                result['current_address'] = d["current_address"]
                result['contact_number'] = d["contact_number"]
                result['employer_name'] = d["employer_name"]
                result['annual_income'] = d["annual_income"]
                result['property_address'] = d["property_address"]
                result['loan_amount'] = d["loan_amount"]
                denormalised_block_list.append(result)
                block = block.get_prev()

        if block is not None:
            data = json.loads(block.data)
            if "AuthorisationTransaction" in data:
                result = {'__type': 'AuthorisationBlock'}
                result['timestamp'] = block.timestamp.isoformat()
                result['previous_hash'] = block.previous_hash
                result['hash'] = block.hash
                result['index'] = block.index
                d = data["AuthorisationTransaction"]
                result['property_address'] = d['property_address']
                result['approval_status'] = d['approval_status']
                denormalised_block_list.append(result)
                block = block.get_prev()

        if block is not None:
            data = json.loads(block.data)
            if "PermitApplicationTransaction" in data:
                result = {'__type': 'PermitApplication'}
                result['timestamp'] = block.timestamp.isoformat()
                result['previous_hash'] = block.previous_hash
                result['hash'] = block.hash
                result['index'] = block.index
                d = data["PermitApplicationTransaction"]
                result["property_address"] = d["property_address"]
                result["seller_details"] = d["seller_details"]
                result["seller_licence_number"] = d["seller_licence_number"]
                denormalised_block_list.append(result)
                block = block.get_prev()

        return denormalised_block_list


def get_block_chain_list(query):
    index = {}
    tails = []
    for block in query:
        index[block.hash] = block
    for block in query:
        block.set_is_head(True)
        try:
            previous_hash = block.previous_hash
            h = index[previous_hash]
            block.set_prev(h)
            block.get_prev().set_is_head(False)
        except:
            tails.append(block)  # is a genesis block
    heads = list(filter(lambda x: x.get_is_head(), query))
    chains = map(lambda head: BlockChain(head), heads)

    return chains


class Role(Enum):
    NONE = -1
    SELLER = 1
    AUTHORITY = 2
    BUYER = 3
    BANK = 4


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# class PermitApplication(db.Model):
#     timestamp = db.Column(db.DateTime, nullable=False)
#     previous_hash = db.Column(db.String(50), index=True)
#     property_address = db.Column(db.String(256), nullable=False)
#     seller_details = db.Column(db.String(256), nullable=False)
#     building_design = db.Column(db.LargeBinary, nullable=False)
#     seller_licence_number = db.Column(db.String(23), nullable=False)
#     hash = db.Column(db.String(50), primary_key=True)

#     def __init__(self, timestamp: datetime, previous_hash: str,
#                  property_address: str, seller_details: str,
#                  building_design: bytes, seller_licence_number: str) -> None:
#         super().__init__()
#         self.timestamp = timestamp
#         self.previous_hash = previous_hash
#         self.property_address = property_address
#         self.seller_details = seller_details
#         self.building_design = building_design
#         self.seller_licence_number = seller_licence_number
#         self.hash = self.hash_block()

#     def hash_block(self):
#         sha = hasher.sha256()
#         base64_bytes = base64.b64encode(self.building_design)
#         base64_message = base64_bytes.decode('utf-8')
#         txt = str(self.timestamp) + str(self.previous_hash) \
#             + str(self.property_address) + str(self.seller_details) \
#             + str(self.building_design) + base64_message + \
#             str(self.seller_licence_number)
#         sha.update(txt.encode('utf-8'))
#         return sha.hexdigest()


# class AuthorisationBlock(db.Model):
#     timestamp = db.Column(db.DateTime, nullable=False)
#     previous_hash = db.Column(db.String(50), index=True)
#     property_address = db.Column(db.String(256), nullable=False)
#     approval_status = db.Column(db.SmallInteger, nullable=False)
#     hash = db.Column(db.String(50), primary_key=True)
#     prev = None

#     def __init__(self, timestamp: datetime, previous_hash: str,
#                  approval_status: bool, property_address: str) -> None:
#         super().__init__()
#         self.timestamp = timestamp
#         self.previous_hash = previous_hash
#         self.property_address = property_address
#         self.approval_status = approval_status
#         self.hash = self.hash_block()

#     def hash_block(self) -> str:
#         sha = hasher.sha256()
#         txt = str(self.timestamp) + str(self.previous_hash) \
#             + str(self.property_address) \
#             + str(1 if self.approval_status else 0)
#         sha.update(txt.encode('utf-8'))
#         return sha.hexdigest()


# class BuyerBlock(db.Model):
#     timestamp = db.Column(db.DateTime, nullable=False)
#     previous_hash = db.Column(db.String(50), index=True)
#     full_name = db.Column(db.String(256), nullable=False)
#     dob = db.Column(db.String(10), nullable=False)
#     current_address = db.Column(db.String(256), nullable=False)
#     contact_number = db.Column(db.String(50), nullable=False)
#     employer_name = db.Column(db.String(256), nullable=False)
#     annual_income = db.Column(db.Numeric, nullable=False)
#     property_address = db.Column(db.String(256), nullable=False)
#     loan_amount = db.Column(db.Numeric, nullable=False)
#     hash = db.Column(db.String(50), primary_key=True)

#     def __init__(self, timestamp: datetime, previous_hash: str,
#                  full_name: str, dob: date, current_address: str,
#                  contact_number: str, employer_name: str,
#                  annual_income: decimal, property_address: str,
#                  loan_amount: decimal) -> None:
#         super().__init__()
#         self.timestamp = timestamp
#         self.previous_hash = previous_hash
#         self.full_name = full_name
#         self.dob = dob
#         self.current_address = current_address
#         self.contact_number = contact_number
#         self.employer_name = employer_name
#         self.annual_income = annual_income
#         self.property_address = property_address
#         self.loan_amount = loan_amount
#         self.hash = self.hash_block()

#     def hash_block(self) -> str:
#         sha = hasher.sha256()
#         txt = "{}{}{}{}{}{}{}{}{}{}{}".format(
#             self.timestamp,
#             self.previous_hash,
#             self.full_name,
#             self.dob,
#             self.current_address,
#             self.contact_number,
#             self.employer_name,
#             self.annual_income,
#             self.property_address,
#             self.loan_amount,
#             self.hash,
#         )
#         sha.update(txt.encode('utf-8'))
#         return sha.hexdigest()


# class BankApproval(db.Model):
#     hash = db.Column(db.String(50), primary_key=True)
#     previous_hash = db.Column(db.String(50), index=True)
#     timestamp = db.Column(db.DateTime, nullable=False)
#     approval_status = db.Column(db.SmallInteger, nullable=False)
#     full_name = db.Column(db.String(256), nullable=False)
#     current_address = db.Column(db.String(256), nullable=False)
#     contact_number = db.Column(db.String(50), nullable=False)
#     dob = db.Column(db.String(10), nullable=False)

#     def __init__(self, previous_hash, timestamp, approval_status, full_name, current_address, contact_number, dob) -> None:
#         super().__init__()
#         self.previous_hash = previous_hash
#         self.timestamp = timestamp
#         self.approval_status = approval_status
#         self.full_name = full_name
#         self.current_address = current_address
#         self.contact_number = contact_number
#         self.dob = dob
#         self.hash = self.hash_block()

#     def hash_block(self) -> str:
#         sha = hasher.sha256()
#         txt = "{}{}{}{}{}{}{}".format(
#             self.previous_hash,
#             self.timestamp,
#             1 if self.approval_status else 0,
#             self.full_name,
#             self.current_address,
#             self.contact_number,
#             self.dob,
#         )
#         sha.update(txt.encode('utf-8'))
#         return sha.hexdigest()


# class SaleFinalisationBlock(db.Model):
#     hash = db.Column(db.String(50), primary_key=True)
#     previous_hash = db.Column(db.String(50), index=True)
#     timestamp = db.Column(db.DateTime, nullable=False)
#     approved = db.Column(db.SmallInteger, nullable=False)

#     def __init__(self, previous_hash, timestamp, approved) -> None:
#         super().__init__()
#         self.previous_hash = previous_hash
#         self.timestamp = timestamp
#         self.approved = approved
#         self.hash = self.hash_block()

#     def hash_block(self) -> str:
#         sha = hasher.sha256()
#         txt = "{}{}{}".format(
#             self.previous_hash,
#             self.timestamp,
#             1 if self.approved else 0,
#         )
#         sha.update(txt.encode('utf-8'))
#         return sha.hexdigest()
