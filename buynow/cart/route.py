from flask import render_template, redirect, request, flash, Blueprint, url_for
from flask_login import login_required, current_user
from buynow.models import CartItem, Item, OrderItem, Order, Warehouse, Shipment
from buynow import db
from buynow.cart.forms import AddToCartForm

cart = Blueprint('cart', '__name__')

@cart.route('/item/<int:item_id>/addtocart', methods=['POST'])
@login_required
def add_to_cart(item_id):
    form = AddToCartForm()
    if form.validate_on_submit():
        item = CartItem.query.filter_by(customer_id=current_user.id, item_id=item_id).first()
        if item:
            flash('That item is already added to your cart', 'warning')
        else:
            cart_item = CartItem(customer_id=current_user.id, item_id=item_id, quantity=form.quantity.data)
            db.session.add(cart_item)
            db.session.commit()
            flash('The item is added to you cart', 'success')
    else:
        flash('Maximum 10 items are add to the cart!', 'danger')
    return redirect(url_for('main.home'))

@cart.route('/cart')
@login_required
def show_cart():
    carts = CartItem.query.filter_by(customer_id=current_user.id).order_by()
    cartedItems = {}
    for cart in carts:
        item = Item.query.get_or_404(cart.item_id)
        cartedItems[item] = cart.quantity
    return render_template('cart.html', cartitems=cartedItems, title="Cart") 

@cart.route('/cart/<int:item_id>/remove', methods=['POST'])
@login_required
def remove_cart_item(item_id):
    item = CartItem.query.filter_by(customer_id=current_user.id, item_id=item_id).first()
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from the cart successfully', 'success')
    return redirect(url_for('cart.show_cart'))

@cart.route('/cart/buy', methods=['GET', 'POST'])
@login_required
def buy_cart_all():
    cartitems = CartItem.query.filter_by(customer_id=current_user.id).first()
    if not cartitems:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('main.home'))
    
    warehouse = Warehouse.query.filter_by(city=current_user.city).first()
    if not warehouse:
        flash('Delivery not possition to you city', 'warning')
        return redirect(url_for('main.home'))
    
    cartitems = CartItem.query.filter_by(customer_id=current_user.id)
    amount = 0
    for cart in cartitems:
        item = Item.query.get_or_404(cart.item_id)
        amount +=  (item.price * cart.quantity)
    
    order = Order(customer_id=current_user.id, order_amount=amount)
    db.session.add(order)
    db.session.commit()

    for cart in cartitems:
        orderitem = OrderItem(order_id=order.id, item_id=cart.item_id, quantity=cart.quantity)
        db.session.add(orderitem)
        db.session.commit()
        
    for cart in cartitems:
        db.session.delete(cart)
        db.session.commit()
    
    shipment = Shipment(order_id=order.id, warehouse_id=warehouse.id)
    db.session.add(shipment)
    db.session.commit()

    flash('Order placed','success')
    
    return redirect(url_for('order.show_order'))

