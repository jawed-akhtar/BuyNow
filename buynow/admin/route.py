from flask import render_template, Blueprint
from flask_login import login_required

admin = Blueprint('admin', '__name__')

@admin.route('/admin/home')
@login_required
def admin_home():
    return render_template('admin/admin_home.html', title='Admin-Home')

