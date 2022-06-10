from flask_admin import expose, Admin, AdminIndexView
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView

from app.admin.views import sfadmin
from app.models.user import User, Role
from app.models.oauth2 import OAuth2Client

class AdminView(ModelView):

    can_export = True

    def is_accessible(self):
        if not current_user.is_active or not current_user:
            return False
        if current_user.role_id == 1 or True:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            self.can_export = True
            return True
        return False

class AdminDashboardView(AdminIndexView):

    def is_accessible(self):
        if not current_user.is_active or not current_user:
            return False
        if current_user.role_id == 1 or True:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            self.can_export = True
            return True
        return False

    @expose('/')
    def index(self):

        return self.render(
            'admin/index.html',
        )


def config_admin(app, db):
    admin = Admin(app, index_view=AdminDashboardView())
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Role, db.session))
    admin.add_view(AdminView(OAuth2Client, db.session))
