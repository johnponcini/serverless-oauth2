import os
from datetime import datetime 
import stripe
from simple_salesforce import Salesforce

from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from flask_login import current_user, login_required

from app.admin.forms import CreateContactForm, CreateDonationForm

sf = Salesforce(instance_url="https://maps501c3--arkustest.lightning.force.com", username="digital@maps.org", password="eu3HxxbyX!J_", security_token="dUdkHC149SfzJkdC0YVXYf0W", domain="test")

sfadmin = Blueprint("sfadmin", __name__)


@sfadmin.route('/create_contact', methods=['GET', 'POST'])
def create_contact():

    if current_user.is_anonymous:
        return redirect(url_for('account.login'))

    if current_user.role_id != 1:
        return render_template('403.html')      
      
    form = CreateContactForm()

    if request.method == "POST":
        sf.Contact.create(
            {
                'FirstName' : form.first_name.data, 
                'LastName': form.last_name.data, 
                'Email': form.email.data,
            }
        )

        return redirect(url_for('main.home'))

    return render_template('admin/create_contact.html', form=form)


@sfadmin.route('/create_donation', methods=['GET', 'POST'])
def create_donation():

    if current_user.is_anonymous:
        return redirect(url_for('account.login'))

    if current_user.role_id != 1:
        return render_template('403.html')      

    form = CreateDonationForm()

    if request.method == "POST":

        account_id = sf.query("SELECT AccountId From Contact WHERE Email = '{}'".format(form.email.data))['records'][0]['Id']

        sf.Opportunity.create(
            {
                'AccountId': account_id,
                'Amount': form.amount.data,
                'Name': 'API Test',
                'Type': 'Donation',
                'StageName': 'Posted',
                'closedate': datetime.now().strftime('%Y-%m-%d')
            }
        )

        return redirect(url_for('main.home'))

    return render_template('admin/create_donation.html', form=form)

