from flask import render_template, redirect, request, url_for, Blueprint, flash
from flask_login import login_required, current_user
from buynow.models import Item, OrderItem
from buynow.admin.item.forms import AddItemForm, UpdateItemForm
from buynow.utility.utilities import save_picture, delete_old_picture
from buynow import db

item = Blueprint('item', '__name__')

@item.route('/admin/items', methods=['GET', 'POST'])
@login_required
def show_items():
    items = Item.query.all()
    return render_template('admin/items.html', title="Items", items=items)

@item.route('/admin/items/new', methods=['GET', 'POST'])
@login_required
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        picture = save_picture(form.image.data, 'product_image', 200, 200)
        
        item = Item(category=form.category.data, description=form.description.data, item_image=picture, price=form.price.data)
        db.session.add(item)
        db.session.commit()
        flash(' New item added in items list', 'success')
        return redirect(url_for('item.add_item'))
    return render_template('admin/new_item.html', title="New Item", form=form)

@item.route('/admin/item/<int:item_id>/update', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    form = UpdateItemForm()
    item = Item.query.get_or_404(item_id)
    if form.validate_on_submit():
        if form.image.data:
            delete_old_picture(item.item_image, 'product_image')
            picture = save_picture(form.image.data, 'product_image', 200, 200)
            item.item_image = picture
        item.category = form.category.data
        item.description = form.description.data
        item.price = form.price.data
        db.session.commit()
        flash('Item is updated successfully', 'success')
        return redirect(url_for('item.update_item', item_id=item.id))
    elif request.method == 'GET':
        form.category.data = item.category
        form.description.data = item.description
        form.price.data = item.price
    image = '../../..' + url_for('static', filename='product_image/' + item.item_image)
    return render_template('admin/update_item.html', item_image=image , form=form)

@item.route('/admin/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    ordered_item = OrderItem.query.filter_by(item_id=item.id).first()
    if ordered_item:
        flash('There is an order placed for that item so cant be delete', 'warning')
        return redirect(url_for('item.show_items'))
    delete_old_picture(item.item_image, 'product_image')
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('item.show_items'))
