from decimal import Decimal
from typing import List
from xmlrpc.client import DateTime
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import AuthorisationBlock, BankApproval, BuyerBlock, SaleFinalisationBlock, User, PermitApplication
from werkzeug.urls import url_parse
from datetime import date, datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(get_next_page_or('index'))
        flash('Invalid username or password')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def parse_permit_status(p):
    try:
        approval_status = p['AuthorisationBlock'].approval_status
    except Exception:
        approval_status = None
    return approval_status


@app.route('/api/permit-application', methods=['GET'])
@login_required
def get_permit_application():
    permits = db.session.query(PermitApplication, AuthorisationBlock)\
        .outerjoin(AuthorisationBlock, AuthorisationBlock.previous_hash == PermitApplication.hash).all()

    permits_mapped = map(lambda p: {
        'timestamp': p['PermitApplication'].timestamp,
        'hash': p['PermitApplication'].hash,
        'property_address': p['PermitApplication'].property_address,
        'seller_details': p['PermitApplication'].seller_details,
        'seller_licence_number': p['PermitApplication'].seller_licence_number,
        'approval_status': parse_permit_status(p),
    }, permits)
    return jsonify(list(permits_mapped))


@app.route('/api/permit-application/<hash>/authority', methods=['PUT'])
@login_required
def set_approval(hash):
    content = request.get_json()
    block = AuthorisationBlock(datetime.utcnow(),
                               hash, content['approved'], content['property_address'])
    db.session.add(block)
    db.session.commit()
    return jsonify({'hash': block.hash})


@app.route('/api/permit-application', methods=['POST'])
@login_required
def create_permit_application():
    file = request.files['file']
    file_data: bytes = file.read()

    property_address = request.form['propertyAddress']
    seller_details = request.form['sellerDetails']
    seller_licence_number = request.form['sellerLicenceNumber']

    permit_application = PermitApplication(datetime.utcnow(
    ), 0, property_address, seller_details, file_data, seller_licence_number)
    db.session.add(permit_application)
    db.session.commit()

    return jsonify({'hash': permit_application.hash})


def get_next_page_or(default):
    next_page = request.args.get('next')
    if next_page and url_parse(next_page).netloc == "":
        return next_page
    return url_for(default)


def get_query():
    return db.session.query(
        PermitApplication,
        AuthorisationBlock,
        BuyerBlock,
        BankApproval,
        SaleFinalisationBlock,
    ).outerjoin(
        AuthorisationBlock, AuthorisationBlock.previous_hash == PermitApplication.hash
    ).outerjoin(
        BuyerBlock, BuyerBlock.previous_hash == AuthorisationBlock.hash
    ).outerjoin(
        BankApproval, BankApproval.previous_hash == BuyerBlock.hash
    ).outerjoin(
        SaleFinalisationBlock, SaleFinalisationBlock.previous_hash == BankApproval.hash
    )


def mapper(p): return [
    {
        '__type': 'PermitApplication',
        'timestamp': p['PermitApplication'].timestamp,
        'previous_hash': p['PermitApplication'].previous_hash,
        'hash': p['PermitApplication'].hash,
        'property_address': p['PermitApplication'].property_address,
        'seller_details': p['PermitApplication'].seller_details,
        'seller_licence_number': p['PermitApplication'].seller_licence_number,
    },
    get_authorisation_block(p),
    get_buyers_block(p),
    get_bank_approval_block(p),
    get_sale_finalisation_block(p),
]


@app.route('/api/v2/permit_applications', methods=['GET'])
@login_required
def get_permit_blocks():
    query = get_query().all()
    results = map(mapper, query)
    return jsonify(list(results))


@app.route('/api/v2/buyer_applications/<hash>', methods=['POST'])
@login_required
def create_buyer_application(hash):
    content = request.get_json()
    block = BuyerBlock(
        timestamp=datetime.utcnow(),
        previous_hash=hash,
        annual_income=Decimal(content['annual_income']),
        contact_number=content['contact_number'],
        current_address=content['current_address'],
        dob=datetime.strptime(content['dob'], '%Y-%m-%d'),
        employer_name=content['employer_name'],
        full_name=content['full_name'],
        loan_amount=Decimal(content['loan_amount']),
        property_address=content['property_address'],
    )
    db.session.add(block)
    db.session.commit()
    return jsonify({'hash': block.hash})


@app.route('/api/v2/permit_applications/available-for-purchase', methods=['GET'])
@login_required
def get_purchaseable_permit_blocks():
    query = get_query().filter(AuthorisationBlock.approval_status == True).all()
    results = map(mapper, query)
    return jsonify(list(results))


@app.route('/api/v2/loan_applications', methods=['GET'])
@login_required
def get_loan_applications():
    query = get_query().filter(BuyerBlock.hash != None).all()
    results = map(mapper, query)
    return jsonify(list(results))


@app.route('/api/v2/loan_applications/<hash>', methods=['PUT'])
@login_required
def approve_loan_application(hash):
    content = request.get_json()
    block = BankApproval(
        approval_status=content['approval_status'],
        contact_number=content['contact_number'],
        current_address=content['current_address'],
        dob=datetime.strptime(content['dob'], '%Y-%m-%d'),
        full_name=content['full_name'],
        previous_hash=hash,
        timestamp=datetime.utcnow(),
    )
    db.session.add(block)
    db.session.commit()
    return jsonify({'hash': block.hash})


# Block checking public
@app.route('/api/v2/check_block/authority/<hash>', methods=['GET'])
def check_block(hash):
    log = ['Validation results:']
    passed = new_func(hash, log)
    color = '\033[92m' if passed else '\033[91m'

    for l in log:
        print(color + 'LOG:\t' + l + '\033[0m')

    return jsonify({
        'log': log,
        'passed': passed,
    })


@app.route('/api/v2/check_block/bank_approval/<hash>', methods=['GET'])
def check_bank_approval_block(hash):
    log = ['Validation results:']
    passed = new_func(hash, log, "LoanApproval")
    color = '\033[92m' if passed else '\033[91m'

    for l in log:
        print(color + 'LOG:\t' + l + '\033[0m')

    return jsonify({
        'log': log,
        'passed': passed,
    })


@app.route('/api/v2/loan_applications/<hash>/finalise', methods=['PUT'])
@login_required
def set_borrower_approval(hash):
    content = request.get_json()
    block = SaleFinalisationBlock(
        previous_hash=hash,
        timestamp=datetime.utcnow(),
        approved=content['approved'],
    )
    # db.session.add(block)
    # db.session.commit()
    return jsonify({'hash': block.hash})


@app.route('/api/v2/permit_applications/<hash>/pdf')
def get_pdf(hash):
    permit_application = db.session.query(PermitApplication).filter(
        PermitApplication.hash == hash).first()
    response = make_response(permit_application.building_design)
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment',
                         filename='%s.pdf' % "Building Plans")
    return response


def new_func(hash: str, log: List, type="AuthorisationBlock"):
    log.append("Looking for existence of block: {}".format(hash))
    try:
        if type == "AuthorisationBlock":
            block = db.session.query(AuthorisationBlock).filter(
                AuthorisationBlock.hash == hash).first()
        else:
            block = db.session.query(BankApproval).filter(
                BankApproval.hash == hash).first()

        log.append("Found block: {}".format(block.hash))
    except:
        log.append("Block not found!")
        return False

    if type == "AuthorisationBlock":
        log.append("Block details: timestamp='{}', previous_hash='{}', property_address: '{}', approval_status: '{}'".format(
            block.timestamp,
            block.previous_hash,
            block.property_address,
            block.approval_status,
        ))
    else:
        log.append("Block details: previous_hash='{}' timestamp='{}' approval_status='{}' full_name='{}' current_address='{}' contact_number='{}' dob='{}'".format(
            block.previous_hash,
            block.timestamp,
            block.approval_status,
            block.full_name,
            block.current_address,
            block.contact_number,
            block.dob,
        ))

    calcualted_hash = block.hash_block()
    log.append(
        "Running hash function on block returns: {}".format(calcualted_hash))

    try:
        assert(hash == calcualted_hash)
        log.append("Hashes match.")
    except AssertionError:
        log.append("Hashes do not match! Record could be tampered with.")
        return False

    return True


def get_authorisation_block(p):
    try:
        block = p['AuthorisationBlock']
        result = {'__type': 'AuthorisationBlock'}
        result['timestamp'] = block.timestamp.isoformat()
        result['previous_hash'] = block.previous_hash
        result['property_address'] = block.property_address
        result['approval_status'] = block.approval_status
        result['hash'] = block.hash
    except Exception:
        result = {}
    return result


def get_buyers_block(p):
    try:
        block = p['BuyerBlock']
        result = {'__type': 'BuyerBlock'}
        result['timestamp'] = block.timestamp.isoformat()
        result['previous_hash'] = block.previous_hash
        result['full_name'] = block.full_name
        result['dob'] = block.dob
        result['current_address'] = block.current_address
        result['contact_number'] = block.contact_number
        result['employer_name'] = block.employer_name
        result['annual_income'] = block.annual_income
        result['property_address'] = block.property_address
        result['loan_amount'] = block.loan_amount
        result['hash'] = block.hash
    except Exception:
        result = {}
    return result


def get_bank_approval_block(p):
    try:
        block = p['BankApproval']
        result = {'__type': 'BankApproval'}
        result['hash'] = block.hash
        result['previous_hash'] = block.previous_hash
        result['timestamp'] = block.timestamp.isoformat()
        result['approval_status'] = block.approval_status
        result['full_name'] = block.full_name
        result['current_address'] = block.current_address
        result['contact_number'] = block.contact_number
        result['dob'] = block.dob
    except Exception:
        result = {}
    return result


def get_sale_finalisation_block(p):
    try:
        block = p['SaleFinalisationBlock']
        result = {'__type': 'SaleFinalisationBlock'}
        result['hash'] = block.hash
        result['previous_hash'] = block.previous_hash
        result['timestamp'] = block.timestamp.isoformat()
        result['approved'] = block.approval_status
    except Exception:
        result = {}
    return result
