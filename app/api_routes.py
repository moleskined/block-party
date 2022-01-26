
import base64
from decimal import Decimal
from typing import List
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import BlockChain, User, Block, get_block_chain_list, MAX_DATA_DISPLAY_LENGTH
from werkzeug.urls import url_parse
from datetime import date, datetime
import json
import sqlalchemy


@app.route('/api/v2/permit_applications', methods=['GET'])
@login_required
# Permit Applications: Get
def get_permit_blocks():
    query = db.session.query(Block).all()
    block_chains = get_block_chain_list(query)
    results = map(lambda bc: bc.flatten(), block_chains)
    return jsonify(list(results))


@app.route('/api/v2/permit-application', methods=['POST'])
@login_required
# Permit Applications: Create
def create_permit_application():
    file = request.files['file']
    file_data: bytes = file.read()
    base64_bytes = base64.b64encode(file_data)
    base64_message = base64_bytes.decode('utf-8')
    d = json.dumps({
        'PermitApplicationTransaction': {
            'property_address': request.form['propertyAddress'],
            'seller_details': request.form['sellerDetails'],
            'seller_licence_number': request.form['sellerLicenceNumber'],
            'building_design': base64_message,
        },
    })
    block = Block(datetime.utcnow(), get_next_id(), "0", d)
    db.session.add(block)
    db.session.commit()
    log_create_block(block)

    return jsonify({'hash': block.hash})


@app.route('/api/v2/permit-application/<hash>/authority', methods=['PUT'])
@login_required
# Authority: Update
def set_approval(hash):
    content = request.get_json()
    d = json.dumps({
        "AuthorisationTransaction": {
            "approval_status": content["approved"],
            "property_address": content["property_address"],
        },
    })
    block = Block(datetime.utcnow(), get_next_id(), hash, d)
    db.session.add(block)
    db.session.commit()
    log_create_block(block)
    return jsonify({'hash': block.hash})


@app.route('/api/v2/permit_applications/available-for-purchase', methods=['GET'])
@login_required
# Buyers: Get
def get_purchaseable_permit_blocks():
    query = db.session.query(Block).all()
    block_chains = get_block_chain_list(query)
    results = []
    for block_chain in block_chains:
        if "AuthorisationTransaction" in block_chain.index and block_chain.index["AuthorisationTransaction"]["approval_status"]:
            flattened = block_chain.flatten()
            results.append(flattened)
    return jsonify(list(results))


@app.route('/api/v2/buyer_applications/<hash>', methods=['POST'])
@login_required
# Buyers: Create
def create_buyer_application(hash):
    content = request.get_json()
    d = json.dumps({
        "BuyerTransaction": {
            "annual_income": int(content["annual_income"]),
            "contact_number": content["contact_number"],
            "current_address": content["current_address"],
            "dob": content["dob"],
            "employer_name": content["employer_name"],
            "full_name": content["full_name"],
            "loan_amount": int(content["loan_amount"]),
            "property_address": content["property_address"],
        },
    })
    block = Block(
        timestamp=datetime.utcnow(),
        index=get_next_id(),
        previous_hash=hash,
        data=d,
    )
    db.session.add(block)
    db.session.commit()
    log_create_block(block)
    return jsonify({'hash': block.hash})


@app.route('/api/v2/loan_applications', methods=['GET'])
@login_required
# Banks: Get
def get_loan_applications():
    query = db.session.query(Block).all()
    block_chains = get_block_chain_list(query)
    results = []
    for block_chain in block_chains:
        if "BuyerTransaction" in block_chain.index:
            flattened = block_chain.flatten()
            results.append(flattened)
    return jsonify(list(results))


@app.route('/api/v2/block/<hash>/validate', methods=['GET'])
@login_required
# All: Get
def validate_block(hash):
    log = []
    title = 'BEGINNING VALIDATION OF BLOCK {}'.format(hash)
    border = "=" * len(title)
    log.append(border)
    log.append(title)
    log.append(border)

    query = db.session.query(Block).all()
    block_chains = get_block_chain_list(query)
    passed = get_block_validation_outcome(hash, log, block_chains)

    if passed:
        title = 'BLOCK {} IS VALID!'.format(hash)
    else:
        title = 'BLOCK {} IS NOT VALID!'.format(hash)
    border = "=" * len(title)
    log.append(border)
    log.append(title)
    log.append(border)
    log.append("")

    for l in log:
        print(l)
    return jsonify({
        'log': log,
        'passed': passed,
    })


@app.route('/api/v2/loan_applications/<hash>', methods=['PUT'])
@login_required
# Banks: Update
def approve_loan_application(hash):
    content = request.get_json()
    d = json.dumps({
        "BankApprovalTransaction": {
            "approval_status": content['approval_status'],
            "contact_number": content['contact_number'],
            "current_address": content['current_address'],
            "dob": content['dob'],
            "full_name": content['full_name'],
        },
    })
    block = Block(
        timestamp=datetime.utcnow(),
        index=get_next_id(),
        previous_hash=hash,
        data=d,
    )
    db.session.add(block)
    db.session.commit()
    log_create_block(block)
    return jsonify({'hash': block.hash})


@app.route('/api/v2/loan_applications/<hash>/finalise', methods=['PUT'])
@login_required
# Seller: Update
def set_borrower_approval(hash):
    content = request.get_json()
    d = json.dumps({
        "SaleFinalisationTransaction": {
            "approved": content['approved'],
        },
    })
    block = Block(
        timestamp=datetime.utcnow(),
        index=get_next_id(),
        previous_hash=hash,
        data=d,
    )
    db.session.add(block)
    db.session.commit()
    log_create_block(block)
    return jsonify({'hash': block.hash})


@app.route('/api/v2/permit_applications/<hash>/pdf')
# All: Get
def get_pdf(hash):
    block = db.session.query(Block).filter(Block.hash == hash).first()
    data = json.loads(block.data)
    permit_application = data["PermitApplicationTransaction"]
    building_design_b64 = permit_application["building_design"]
    building_design_bytes = base64.b64decode(building_design_b64)
    response = make_response(building_design_bytes)
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment',
                         filename='%s.pdf' % "Building Plans")
    return response


@app.route('/api/v2/block/all')
def dump_block_chains():
    result_str = "# Blockchain Dump\n"
    query = db.session.query(Block).all()
    block_chains = get_block_chain_list(query)
    i = 1
    for block_chain in block_chains:
        next_block = block_chain.get_head()
        result_str += "\n## Blockchain {0}\n\n".format(i)
        while next_block is not None:
            result_str += "{}\n".format(next_block)
            next_block = next_block.get_prev()
            if next_block is not None:
                result_str += "                        |\n                        |\n                        |\n"
        i += 1

    print(result_str)
    response = make_response(result_str)
    response.headers.set('Content-Type', 'text/plain; charset=utf-8')
    return response


def get_block_validation_outcome(block_hash: str, log: List, block_chains: map):
    # Find block in chains
    for block_chain in block_chains:
        try:
            block: Block = block_chain.index['__by_hash'][block_hash]
        except KeyError:
            pass

    try:
        current_block = block
        log.append("Found BLOCK")
    except UnboundLocalError:
        log.append("Block not found!")
        return False

    log.append("")
    log.append("Validating Blockchain")
    log.append("---------------------")

    # Add each block to a stack for validation. We will validate
    # each block from the first, to the requested to check hash values
    todo_stack = []
    while current_block is not None:
        todo_stack.append(current_block)
        current_block = current_block.get_prev()
    log.append(str(todo_stack))

    prev_hash = "0"
    curr_block: Block = todo_stack.pop()
    while curr_block is not None:
        log.append("")
        log.append("Block data on record")
        log.append("--------------------")
        str_block = str(curr_block).split('\n')
        for line in str_block:
            log.append("" + line)

        stored_hash = curr_block.hash
        actual_hash = curr_block.hash_block()
        log.append("")
        log.append("Calculating hash from data and comparing to stored")
        log.append("--------------------------------------------------")
        log.append("Hash String: '{0}' # May be truncated".format(
            curr_block.get_hash_text()[:MAX_DATA_DISPLAY_LENGTH]))
        log.append("Recalculated Hash: {0}".format(actual_hash))
        try:
            assert(actual_hash == stored_hash)
            log.append("Hash is VALID!".format(actual_hash))
        except AssertionError:
            log.append("Hash is NOT VALID!".format(actual_hash))
            return False

        log.append("")
        log.append("Verifying block against previous hash")
        log.append("-------------------------------------")
        if prev_hash == "0":
            log.append("Skipped because block is Genesis Block")
        else:
            original_hash = curr_block.previous_hash
            log.append("Stored Previous Hash: {0}".format(
                curr_block.previous_hash))
            curr_block.previous_hash = prev_hash
            log.append("Calculated Previous Hash: {0}".format(
                curr_block.previous_hash))
            log.append("Recalculated Hash: {0}".format(
                curr_block.hash_block()))
            try:
                assert(original_hash == curr_block.previous_hash)
                log.append("Hash is VALID!".format(actual_hash))
            except AssertionError:
                log.append("Hash is NOT VALID!".format(actual_hash))
                return False

        prev_hash = curr_block.hash
        try:
            curr_block = todo_stack.pop()
            log.append("Checking next in chain…")
        except IndexError:
            curr_block = None

    return True


def get_next_id() -> int:
    result = db.session.execute(
        "SELECT MAX(`index`) AS Highest FROM Block;").first()
    try:
        next = result['Highest'] + 1
    except TypeError:
        next = 0
    return next


def log_create_block(block):
    log = []
    title = 'CREATING BLOCK {}'.format(block.hash)
    border = "=" * len(title)
    log.append(border)
    log.append(title)
    log.append(border)
    str_block = str(block).split('\n')
    for line in str_block:
        log.append("" + line)
    for l in log:
        print(l)
