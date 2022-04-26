from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.models.user import User
from app.models.oauth2 import OAuth2Client

def config_admin(app, db):
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(OAuth2Client, db.session))
