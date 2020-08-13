from flask import Flask, render_template, Blueprint
from buynow.models import Item
from buynow.cart.forms import AddToCartForm
from buynow.order.forms import OrderForm

main = Blueprint('main', '__name__')

@main.route("/")
@main.route("/home")
def home():
    items = Item.query.all()
    cartForm = AddToCartForm()
    orderForm = OrderForm()
    return render_template('home.html', title="BuyNow-Home", items=items, cartForm=cartForm, orderForm=orderForm)