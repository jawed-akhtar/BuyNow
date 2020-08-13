from flask import render_template, url_for, flash, redirect, request, Blueprint
from buynow.login.forms import LoginUserForm
from buynow.models import Customer
from buynow import bcrypt
from flask_login import login_user, logout_user, current_user

login = Blueprint('login', '__name__')

@login.route('/login', methods=['GET', 'POST'])
def loginUser():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginUserForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else: 
            flash('Login Unsucessfull, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@login.route('/logout')
def logoutUser():
    logout_user()
    return redirect(url_for('main.home'))