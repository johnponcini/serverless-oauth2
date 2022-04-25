from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.models import User

def config_admin(app, db):
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
