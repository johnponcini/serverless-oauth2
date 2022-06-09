from app import create_app

app = create_app(
    {
        "SECRET_KEY": "secret",
        "OAUTH2_REFRESH_TOKEN_GENERATOR": True,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://admin:ubQMnSvN6LHc4nQ!@oauth2.cswiy5vmwmww.us-west-2.rds.amazonaws.com",
    }
)
