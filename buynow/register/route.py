from flask import render_template, url_for, flash, redirect, request, Blueprint
from buynow import db, bcrypt
from buynow.models import Customer
from buynow.register.forms import RegistrationForm
from flask_login import current_user

register = Blueprint('register', '__name__')

@register.route('/register', methods=['GET', 'POST'])
def registerUser():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(name=form.name.data, email=form.email.data, password=hashed_pw, city=form.city.data)
        db.session.add(customer)
        db.session.commit()

        flash('Account created Successfuly, Login now', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)