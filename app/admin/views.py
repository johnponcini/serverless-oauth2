import os
import time
import stripe
from simple_salesforce import Salesforce

from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from flask_login import current_user, login_required

from app.admin.forms import CreateContactForm, CreateDonationForm

sf = Salesforce(instance_url="https://maps501c3--arkustest.lightning.force.com", username="digital@maps.org", password="eu3HxxbyX!J_", security_token="dUdkHC149SfzJkdC0YVXYf0W", domain="test")

admin = Blueprint("admin", __name__)


@admin.route("/create-customer", methods=["GET", "POST"])
def create_customer():
    form = CreateContactForm

    sf.Contact.create(
        {
            'FirstName' : form.first_name.data, 
            'LastName': form.last_name.data, 
            'Email': form.email.data,
        }
    )

    return redirect(url_for('admin'))
