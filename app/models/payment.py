from app import db
from app.models.user import User



class Payment(db.Model):
    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="payment", lazy="dynamic")