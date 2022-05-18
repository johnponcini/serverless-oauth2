from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    RadioField,
    EmailField,
    IntegerField
)
from wtforms.validators import Email, EqualTo, InputRequired, Length

class CreateContactForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(1, 64)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(1, 64)])
    email = EmailField("Email", validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField("Create Contact")

class CreateDonationForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Length(1, 64), Email()])
    amount = IntegerField("Amount", validators=[InputRequired()])
    submit = SubmitField("Donate")