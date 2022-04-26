from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from authlib.jose.errors import BadSignatureError

from app import db
from app.oauth.signature import get_jws_token, verify_jws_token
from config import login_manager


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))

    @property
    def password(self):
        raise AttributeError("`password` is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=604800):
        """Generate a confirmation token to email a new user."""

        return get_jws_token({"confirm": self.id}, expiration)

    def generate_email_change_token(self, new_email, expiration=3600):
        """Generate an email change token to email an existing user."""
        return get_jws_token(
            {"change_email": self.id, "new_email": new_email}, expiration
        )

    def generate_password_reset_token(self, expiration=3600):
        """
        Generate a password reset change token to email to an existing user.
        """
        return get_jws_token({"reset": self.id}, expiration)

    def confirm_account(self, token):
        """Verify that the provided token is for this user's id."""
        try:
            data = verify_jws_token(token)
        except BadSignatureError:
            return False
        if data.get("confirm") != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def change_email(self, token):
        """Verify the new email for this user."""
        try:
            data = verify_jws_token(token)
        except BadSignatureError:
            return False
        if data.get("change_email") != self.id:
            return False

        new_email = data.get("new_email")
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        db.session.commit()
        return True

    def reset_password(self, token, new_password):
        """Verify the new password for this user."""
        try:
            data = verify_jws_token(token)
        except BadSignatureError:
            return False
        if data.get("reset") != self.id:
            return False

        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True
        
    def __repr__(self):
        return "<User '%s'>" % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
