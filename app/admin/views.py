from datetime import datetime 

from flask import Blueprint, request, session, url_for
from flask import render_template, redirect
from flask_login import current_user

from app.admin.forms import CreateContactForm, CreateDonationForm

from config import sf

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

        contact_id = sf.query("SELECT Id From Contact WHERE Email = '{}'".format(form.email.data))['records'][0]['Id']

        contact = sf.Contact.get(contact_id)

        account_id = contact['AccountId']

        sf.Opportunity.create(
            {
                'AccountId': account_id,
                'Amount': form.amount.data,
                'Name': 'API Test',
                'Type': 'Donation',
                'StageName': 'Posted',
                'closedate': datetime.now().strftime('%Y-%m-%d'),
                'CampaignId': '7012f000000bOFfAAM',
                'Purpose__c': 'Unrestricted',
                'Tender_Type__c': 'Stripe',
                'Platform_Source__c': 'MAPSi',
                'Donation_Page__c': 'Test Page'
            }
        )

        return redirect(url_for('main.home'))

    return render_template('admin/create_donation.html', form=form)

