from flask import render_template, redirect, request, url_for, Blueprint, flash
from flask_login import current_user, login_required
from buynow.models import Order, OrderItem, Item, Shipment, Warehouse
from buynow.order.forms import OrderForm
from buynow import db

order = Blueprint('order', '__name__')

@order.route('/order')
@login_required
def show_order():
    orders = Order.query.filter_by(customer_id=current_user.id).first()
    if not orders:
        flash('You have placed any order yet!', 'warning')
        return redirect(url_for('main.home'))
    
    orders = Order.query.filter_by(customer_id=current_user.id).order_by(Order.order_date.desc())
    shipments = {}
    orderList = {}
    for order in orders:
        orderitems = OrderItem.query.filter_by(order_id=order.id)
        orditems = []
        for item in orderitems:
            i = Item.query.get_or_404(item.item_id)
            pair = [i, item.quantity]
            orditems.append(pair)
        orderList[order] = orditems
        shipment = Shipment.query.filter_by(order_id=order.id).first()
        shipments[order] = shipment.shipment_date
    return render_template('order.html', orderList=orderList, shipments=shipments)

@order.route('/item/<int:item_id>/order', methods=['GET', 'POST'])
@login_required
def place_order(item_id):
    form = OrderForm()
    if form.validate_on_submit():
        warehouse = Warehouse.query.filter_by(city=current_user.city).first()
        if not warehouse:
            flash('Delivery not possition to you city', 'warning')
            return redirect(url_for('main.home'))

        item = Item.query.get_or_404(item_id)
        amount = (item.price * form.quantity.data)
    
        order = Order(customer_id=current_user.id, order_amount=amount)
        db.session.add(order)
        db.session.commit()

        orderitem = OrderItem(order_id=order.id, item_id=item_id, quantity=form.quantity.data)
        db.session.add(orderitem)
        db.session.commit()

        shipment = Shipment(order_id=order.id, warehouse_id=warehouse.id)
        db.session.add(shipment)
        db.session.commit()
        flash('Order placed', 'success')
        return redirect(url_for('order.show_order'))
    return redirect(url_for('main.home'))