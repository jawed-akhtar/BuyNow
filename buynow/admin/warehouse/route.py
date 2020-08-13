from flask import render_template, redirect, request, url_for, Blueprint, flash
from flask_login import login_required, current_user
from buynow.models import Warehouse
from buynow.admin.warehouse.forms import AddWarehouseForm, UpdateWarehouseForm
from buynow import db

warehouse = Blueprint('warehouse', '__name__')

@warehouse.route('/admin/warehouses', methods=['GET', 'POST'])
@login_required
def show_warehouses():
    warehouses = Warehouse.query.all()
    return render_template('admin/warehouses.html', title="Warehouses", warehouses=warehouses)

@warehouse.route('/admin/warehouses/new', methods=['GET', 'POST'])
@login_required
def add_warehouse():
    form = AddWarehouseForm()
    if form.validate_on_submit():
        warehouse = Warehouse(city=form.city.data)
        db.session.add(warehouse)
        db.session.commit()
        flash(' New warehouse added in warehouses list', 'success')
        return redirect(url_for('warehouse.add_warehouse'))
    return render_template('admin/warehouse_form.html', title="New warehouse", form=form, opr='Add New')

@warehouse.route('/admin/warehouse/<int:warehouse_id>/update', methods=['GET', 'POST'])
@login_required
def update_warehouse(warehouse_id):
    form = UpdateWarehouseForm()
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    if form.validate_on_submit():
        warehouse.city = form.city.data
        db.session.commit()
        flash('Warehouse is updated successfully', 'success')
        return redirect(url_for('warehouse.update_warehouse', warehouse_id=warehouse.id))
    elif request.method == 'GET':
        form.city.data = warehouse.city
    return render_template('admin/warehouse_form.html', title="Update warehouse", opr='Update' , form=form)

@warehouse.route('/admin/warehouse/<int:warehouse_id>/delete', methods=['POST'])
@login_required
def delete_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    if warehouse.shipments:
        flash('There is an order placed for that warehouse so cant be delete', 'warning')
        return redirect(url_for('warehouse.show_warehouses'))
    db.session.delete(warehouse)
    db.session.commit()
    return redirect(url_for('warehouse.show_warehouses'))
