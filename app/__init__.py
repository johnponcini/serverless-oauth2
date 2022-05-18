from flask import Flask
from sqlalchemy import MetaData, create_engine
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy(metadata=MetaData())


def create_app(config_name="development"):
    if config_name == "development":
        print("App is in DEV MODE!")
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app, db)


    # OAuth2
    from .oauth import config_oauth

    config_oauth(app)

    # Blueprints
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .oauth import oauth as oauth_blueprint

    app.register_blueprint(oauth_blueprint, url_prefix="/oauth")

    from .account import account as account_blueprint

    app.register_blueprint(account_blueprint, url_prefix="/account")

    # Admin
    from .admin import admin as admin_blueprint

    from .admin import config_admin

    config_admin(app, db)

    return app
