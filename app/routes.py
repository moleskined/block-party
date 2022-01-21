from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import AuthorisationBlock, User, PermitApplication
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

@app.route('/api/properties/authorised', methods=['GET'])
@login_required
def get_authorised_properties():
    query = db.session.query(PermitApplication, AuthorisationBlock)\
        .outerjoin(AuthorisationBlock, AuthorisationBlock.previous_hash == PermitApplication.hash)\
            .filter(AuthorisationBlock.approval_status).all()
    results = map(lambda p: {
        'timestamp': p['AuthorisationBlock'].timestamp,
        'previous_hash': p['AuthorisationBlock'].previous_hash,
        'property_address': p['AuthorisationBlock'].property_address,
        'approval_status': p['AuthorisationBlock'].approval_status,
        'hash': p['AuthorisationBlock'].hash,
    }, query)
    return jsonify(list(results))