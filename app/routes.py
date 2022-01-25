import base64
from decimal import Decimal
from typing import List
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Block
from werkzeug.urls import url_parse
from datetime import date, datetime
import json


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


def get_next_page_or(default):
    next_page = request.args.get('next')
    if next_page and url_parse(next_page).netloc == "":
        return next_page
    return url_for(default)


