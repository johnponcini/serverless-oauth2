from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    TextAreaField,
    SelectField,
    SubmitField,
    RadioField,
    EmailField,
)

from wtforms.validators import Email, EqualTo, InputRequired, Length, URL

from app.models import OAuth2Client

class RegisterClientForm(FlaskForm):
    client_name = StringField("Client Name", validators=[InputRequired(), Length(1, 64)])
    client_uri = StringField("Client URI", validators=[InputRequired(), URL()])
    scope = StringField("Allowed Scopes", validators=[InputRequired(), Length(1, 64)])
    redirect_uri = TextAreaField("Redirect URIs", validators=[InputRequired()])
    grant_type = TextAreaField("Grant Type", validators=[InputRequired()])
    response_type = TextAreaField("Response Type", validators=[InputRequired()])
    token_endpoint_auth_method = SelectField("Token Enpoint Auth Method", choices=[
        ("client_secret_basic", "client_secret_basic"), 
        ("client_secret_post", "client_secret_post"),
        ("none", "none")
    ])
    submit = SubmitField("Create Client")

class AuthorizeConsentForm(FlaskForm):
    confirm = BooleanField("Yes")
    submit = SubmitField("Allow")
