from datetime import datetime, timedelta
from buynow import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_customer(customer_id):
    return Customer.query.get(int(customer_id))

def shipDate():
    return datetime.utcnow() + timedelta(days=10)

class Customer(db.Model, UserMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.png")
    city = db.Column(db.String(25), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    orders = db.relationship('Order', backref='buyer', lazy=True)
    cart_item = db.relationship('CartItem', backref='buyer', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'customer_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            customer_id = s.loads(token)['customer_id']
        except:
            return None
        return Customer.query.get(customer_id)
    
    def __repr__(self):
        return f"Customer('{self.id}', '{self.name}', '{self.admin}', '{self.email}', '{self.image}', '{self.city}')"


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    order_amount = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='orderno', lazy=True)
    shipment_details = db.relationship('Shipment', backref='orderno', lazy=True)
    
    def __repr(self):
        return f"Order('{self.id}', '{self.order_date}', '{self.order_amount}', '{self.customer_id}')"

class OrderItem(db.Model):
    __tablename__ = 'orderitems'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"OrderItem('{self.order_id}', '{self.item_id}', '{self.quantity}')"

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    item_image = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    order_item = db.relationship('OrderItem', backref='orderby',lazy=True)
    cart = db.relationship('CartItem', backref='item', lazy=True)

    def __repr(self):
        return f"Item('{self.id}', '{self.category}', '{self.description}', '{self.item_image}', '{self.price}')"

class Shipment(db.Model):
    __tablename__ = 'shipments'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), primary_key=True)
    shipment_date = db.Column(db.DateTime, default=shipDate, nullable=False)

    def __repr__(self):
        return f"Shipment('{self.order_id}', '{self.warehouse_id}', '{self.shipment_date}')"

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    city = db.Column(db.String(25), unique=True, nullable=False)
    shipment = db.relationship('Shipment', backref='warehouse', lazy=True)

    def __repr__(self):
        return f"Warehouse('{self.id}', '{self.city}')"

class CartItem(db.Model):
    __tablename__ = 'cartitems'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"CartItem('{self.customer_id}', '{self.item_id}', '{self.quantity}')"

db.create_all()
