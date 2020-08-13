from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user
from buynow.customer.forms import UpdateAccountForm
from buynow import db
from buynow.utility.utilities import save_picture, delete_old_picture

customer = Blueprint('customer', '__name__')

@customer.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            if current_user.image != 'default.png':
                delete_old_picture(current_user.image, 'profile_pic')
            picture = save_picture(form.profile_pic.data, 'profile_pic', 125, 125)
            current_user.image = picture
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.city = form.city.data
        db.session.commit()
        flash('Account updated successfully', 'success')
        return redirect(url_for('customer.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.city.data = current_user.city
    image_file = '../' + url_for('static', filename='profile_pic/' + current_user.image)
    
    return render_template('account.html', title='Account', profile_pic=image_file, form = form)