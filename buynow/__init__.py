import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://jawed-akhtar:jawedakhtar@localhost:5432/buynow"
app.config['SECRET_KEY'] = '3b5291d1044d67383328d4861e0e840b'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "mybuynowapp@gmail.com"
app.config['MAIL_PASSWORD'] = "buynow123"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login.loginUser'
login_manager.login_message_category = 'info'
mail = Mail(app)

from buynow.main.route import main
from buynow.register.route import register
from buynow.login.route import login
from buynow.customer.route import customer
from buynow.reset.route import reset
from buynow.admin.route import admin
from buynow.admin.item.route import item
from buynow.admin.warehouse.route import warehouse
from buynow.cart.route import cart
from buynow.order.route import order

app.register_blueprint(main)
app.register_blueprint(register)
app.register_blueprint(login)
app.register_blueprint(customer)
app.register_blueprint(reset)
app.register_blueprint(admin)
app.register_blueprint(item)
app.register_blueprint(warehouse)
app.register_blueprint(cart)
app.register_blueprint(order)
