import os
import stripe

from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
from flask_s3 import FlaskS3
from flask_authorize import Authorize

from simple_salesforce import Salesforce

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask Extensions
csrf = CSRFProtect()
mail = Mail()
s3 = FlaskS3()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "account.login"
authorize = Authorize()

# Environment variables
if os.path.exists("config.env"):
    print("Importing environment from .env file")
    for line in open("config.env"):
        var = line.strip().split("=")
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace('"', "")


# Salesforce Integration

sf = Salesforce(
    instance_url=os.environ.get('SF_INSTANCE_URL'),
    username=os.environ.get('SF_USERNAME'), 
    password=os.environ.get('SF_PASSWORD'), 
    security_token=os.environ.get('SF_SECURITY_TOKEN'), 
    domain=os.environ.get('SF_DOMAIN')
)

# Stripe Configuration
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class Config:
    APP_NAME = os.environ.get("APP_NAME")

    if os.environ.get("SECRET_KEY"):
        SECRET_KEY = os.environ.get("SECRET_KEY")
    else:
        SECRET_KEY = "SECRET_KEY_ENV_VAR_NOT_SET"
        print("SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT") or 587
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") or True
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") or False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("EMAIL_SENDER")

    # Admin account
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "password"
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
    EMAIL_SUBJECT_PREFIX = "[{}]".format(APP_NAME)
    EMAIL_SENDER = "{app_name} <{email}>".format(
        app_name=APP_NAME, email=MAIL_DEFAULT_SENDER
    )

    # AWS
    FLASKS3_BUCKET_NAME = os.environ.get("FLASKS3_BUCKET_NAME")
    FLASKS3_URL_STYLE = os.environ.get("FLASKS3_URL_STYLE")
    FLASKS3_BUCKET_DOMAIN = os.environ.get("FLASKS3_BUCKET_DOMAIN")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    @staticmethod
    def init_app(app, db):
        # Create tables if they do not exist already
        @app.before_first_request
        def create_tables():
            db.create_all()

        db.init_app(app)
        mail.init_app(app)
        login_manager.init_app(app)
        csrf.init_app(app)
        s3.init_app(app)
        Migrate(app, db)
        CORS(app)
        authorize.init_app(app)


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SSL_DISABLE = (os.environ.get("SSL_DISABLE") or "True") == "True"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get("SECRET_KEY"), "SECRET_KEY IS NOT SET!"


config = {"development": DevelopmentConfig, "production": ProductionConfig}
