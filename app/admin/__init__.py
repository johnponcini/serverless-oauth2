from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models.user import *

def config_admin(app, db):
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
