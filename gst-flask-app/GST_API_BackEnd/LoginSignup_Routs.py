from flask import request, redirect, url_for, make_response, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash
from GST_API_BackEnd import GST_API, Database, GetEncryption
from GST_API_BackEnd.models import User


@GST_API.route('/')
def home():
    return render_template("Home.html")


@GST_API.route('/login-check', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Wrong Password or Email')
        return redirect(url_for('home'))

    if user.role == "Tax_Payer":
        res = make_response(redirect(url_for('tax_payer_home', id=user.id)))
        res.set_cookie('SiteCookie', GetEncryption(user.id), max_age=60 * 60 * 24)
        return res

    elif user.role == "Accountant":
        res = make_response(redirect(url_for('accountant_home', id=user.id)))
        res.set_cookie('SiteCookie', GetEncryption(user.id), max_age=60 * 60 * 24)
        return res


@GST_API.route('/signup-check', methods=['POST', 'GET'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Account already exists')
        return redirect(url_for('home'))

    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

    Database.session.add(new_user)
    Database.session.commit()
    res = make_response(redirect(url_for('tax_payer_home', id=new_user.id)))
    res.set_cookie('SiteCookie', GetEncryption(new_user.id), max_age=60 * 60 * 24)
    return res
