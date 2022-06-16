import os
from nameparser import HumanName
from datetime import datetime

import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

from simple_salesforce import Salesforce

sf = Salesforce(instance_url="https://maps501c3--arkustest.lightning.force.com", username="digital@maps.org", password="eu3HxxbyX!J_", security_token="dUdkHC149SfzJkdC0YVXYf0W", domain="test")


class Contact:

    def __init__(self, email, name, address):
        '''
        '''
        self.id = self.search(email)

        if not self.id:
            self.create(email, HumanName(name), address)


    def search(self, email):
        query = sf.query(
            "SELECT Id From Contact WHERE Email = '{}'".format(email)
        )
        if query.get('totalSize') == 0:
            return None
        else:
            return query['records'][-1]['Id']


    def create(self, email, name, address):
        first_name = name.first.capitalize()
        last_name = name.last.capitalize()

        if not first_name:
            first_name = '_'

        if not last_name:
            last_name = '_'
        

        sf.Contact.create(
            {
                'FirstName' : first_name, 
                'LastName' : last_name, 
                'Email' : email,
                'MailingCity' : address['city'],
                'MailingCountry' : address['country'], 
                'MailingStreet' : address['line1'],
                'MailingPostalCode' : address['postal_code']
            }
        )

class Opportunity:
    '''
    A container to define donations and associated donation functions.
    '''
    def __init__(self, email, amount):
        '''
        '''
        
        contact_id = sf.query("SELECT Id From Contact WHERE Email = '{}'".format(email))['records'][-1]['Id']

        contact = sf.Contact.get(contact_id)

        account_id = contact['AccountId']

        sf.Opportunity.create(
            {
                'AccountId': account_id,
                'Amount': amount,
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
