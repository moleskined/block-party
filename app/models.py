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
    """
    A single Block within a Blockchain. Will be persisted in the local database.
    """
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
        """Gets the text to be hashed in a standardised format"""
        return "{}{}{}{}".format(
            self.timestamp, self.index, self.previous_hash, self.data)

    def hash_block(self):
        """Function for generating Block hashes"""
        sha = hasher.sha256()
        txt = self.get_hash_text()
        sha.update(txt.encode('utf-8'))
        return sha.hexdigest()

    def set_prev(self, block):
        """Gets the previous block when this Block is part of a Blockchain instance"""
        self.previous_instance = block

    def get_prev(self):
        """Sets the previous block when this Block is part of a Blockchain instance"""
        return self.previous_instance

    def set_is_head(self, is_head):
        """Sets that this Block is the first in the chain"""
        self.is_head = is_head

    def get_is_head(self):
        """Is the first in the chain?"""
        return self.is_head

    def __repr__(self) -> str:
        return self.hash

    def __str__(self) -> str:
        """Overrides to allow pretty-printing of Blocks to the console"""
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
    """
    A class for representing the Blockhain, and generating one from a
    database query. Responsible for rebulding the chains and establishing
    order and precedence.
    """
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
        """
        Messy, but necessary as I implemented incorrectly the first time around
        and now the UI layer expects a certain data structure.
        """
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
    """
    Utility function for parsing a query and returning a
    collection of Blockchains
    """
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
