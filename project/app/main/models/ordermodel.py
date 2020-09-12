from .. import db
import datetime

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    order_date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    order_status = db.Column(db.String(70))
    order_value = db.Column(db.Float)
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"), unique = True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))


class OrderProducts(db.Model):
    __tablename__ = "order_products"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer)
    cost = db.Column(db.Float)
    db.UniqueConstraint("product_id", "order_id")
    db.CheckConstraint(quantity>0)


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pay_method = db.Column(db.String(50))
    pay_amount = db.Column(db.Float)
    pay_reference = db.Column(db.String(100), unique=True, nullable=True)



