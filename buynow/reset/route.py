from flask import render_template, redirect, flash, url_for, Blueprint
from flask_login import current_user
from buynow.reset.forms import ResetRequestForm, ResetPasswordForm
from buynow.models import Customer
from buynow.utility.utilities import send_reset_email
from buynow import bcrypt, db


reset = Blueprint('reset', '__name__')

@reset.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        send_reset_email(customer)
        flash('An email has been send with instructions to reset your password','info')
        return redirect(url_for('login.loginUser'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@reset.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    customer = Customer.verify_reset_token(token)
    if customer is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login.loginUser'))
    return render_template('reset_token.html', title="Reset Password", form=form)