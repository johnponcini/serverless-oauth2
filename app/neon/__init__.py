import os
from nameparser import HumanName
from datetime import datetime, timedelta
from iso3166 import countries

import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

from app.neoncrm import NEON
from app.neon import util

neon = NEON('maps', os.getenv('NEON_KEY'))

COUNTRIES = neon_countries = neon.properties.get_countries().json()
STATES = neon.properties.get_stateProvinces().json()


class Account:
    '''
    Container to define user accounts and associated account functions.
    '''
    def __init__(self, email, name=None, source=None, origin=None, **kwargs):
        '''
        '''
        self.accountId = self.search(email)
        custom_fields = self.get_custom_fields(**kwargs)

        #Check if there's an existing account in NEON
        if not self.accountId:
            self.accountId = self.create(
                email, HumanName(name), source, origin, custom_fields
            )
        elif custom_fields:
             self.update(self.accountId, custom_fields)


    def search(self, email):
        '''
        Search Neon for accounts with the provided email. Return the first
        account ID if there is exactly one. Otherwise, return a null object. 
        '''
        accounts = neon.accounts.search(
            outputFields=['Account ID'],
            searchFields=[
                {
                    'field': 'Email',
                    'operator': 'EQUAL',
                    'value': email,
                }
            ],
            pagination={
                'currentPage': 0,
                'pageSize': 200
            }
        )
        total_results = accounts.json()['pagination']['totalResults']

        if total_results == 0:
            return None
        else:
            return accounts.json()['searchResults'][-1]['Account ID']


    def create(
        self, email, name, source, origin, custom_fields
    ):
        '''
        Construct the account object. Create an account in Neon. Return the
        account ID from the Neon response object.
        '''
        first_name = name.first.capitalize()
        last_name = name.last.capitalize()

        if not first_name:
            first_name = '_'

        if not last_name:
            last_name = '_'

        account = {}
        account["primaryContact"] = {
            "firstName": first_name,
            "lastName": last_name,
            'email1' : email
        }
        account['source'] = self.format_source(source)
        account['origin'] = {'originDetail': origin}
        account['accountCustomFields'] = custom_fields

        try:
            return neon.accounts.create(individualAccount=account).json()['id']

        except:
            return 

    def update(self, accountId, custom_fields):
        '''
        Update an account in Neon provided the account ID.
        '''
        account = {'accountCustomFields' : custom_fields}
        print(account)
        call = neon.accounts.update(accountId=accountId, individualAccount=account)
        print(call.json())

    def format_source(self, source):
        if source == "Stripe Checkout":
             return {'id' : '910'}
        else:
             return {'id' : '910'}


    def get_custom_fields(self, **kwargs):
        custom_fields = []
        if kwargs.get('bulletin'):
            date = datetime.strftime(datetime.now(), '%m/%d/%Y')
            custom_fields.append(self.format_field('361', date))

        address = kwargs.get('address')
        if address:
            custom_fields.extend(util.add_bulletin_fields(address))
    
        if 'newsletter' in kwargs.items():
            if kwargs['newsletter'] == 'Yes':
                custom_fields.append(self.format_field('162', '602', True))
            else:
                custom_fields.append(self.format_field('162', '728', True))
        if 'program_updates' in kwargs.items():
            if kwargs['program_updates'] == 'Yes':
                custom_fields.append(self.format_field('352', 'GO'))
            else:
                custom_fields.append(self.format_field('352', 'STOP'))
        if custom_fields == []:
            return None
        else:
            return custom_fields


    def format_field(self, id, value, option=False):
        if option:
            return {'id': id, 'optionValues': [{'id': value}]}
        else:
            return {'id': id, 'value': value}

    def get_id(self):
        return self.accountId


class Address:
    '''
    '''
    def __init__(self, city, country, line1, line2, postal_code, state=None):
        '''
        '''
        self.city = city
        self.country = self.format_country(country)
        self.line1 = line1
        self.line2 = line2
        self.postal_code = postal_code
        self.territory = None

        if self.country['id'] in {'1', '2'}:
            self.state = self.format_state(state)
        else:
            self.state = None
            self.territory = state

        self.address = self.get()


    def add(self, accountId):
        address = neon.addresses.create(
            accountId=accountId,
            **self.address,
        )
        return address.json()


    def get(self):
        address = {
            'addressLine1' : self.line1,
            'addressLine2' : self.line2,
            'city' : self.city,
            'country' : self.country,
            'zipCode' : self.postal_code
        }
        if self.state:
            address['stateProvince'] = self.state
        elif self.territory:
            address['territory'] = self.territory
        return address


    def format_country(self, country):
        '''
        '''
        country = countries.get(country).name
        
        for neon_country in COUNTRIES:
            if country == neon_country['name']:
                return neon_country
        return None

     
    def format_state(self, state):
        '''
        '''
        for neon_state in STATES:
            if state in {neon_state['code'], neon_state['name']}:
                return neon_state
        return None
    

class Donation:
    '''
    A container to define donations and associated donation functions.
    '''
    def __init__(
        self, allocation, amount, campaign, charge,
        customer, fund, method, source, **kwargs
    ):
        '''
        '''
        self.customer = stripe.Customer.retrieve(customer)

        self.account_id = self.get_account_id(self.customer['email'])
        self.acknowledgee = {
            'accountId' : self.account_id,
            'email' : self.customer['email'],
            'name' : self.customer['name']
        }
        self.allocation = util.get_allocation(allocation)
        self.amount = amount
        self.anonymous = 'No'
        self.campaign = util.get_campaign(campaign)
        self.custom_fields = self.get_custom_fields(**kwargs)
        self.date = datetime.strftime(datetime.now() - timedelta(hours=8), '%Y-%m-%d')
        self.fund = fund
        self.method = util.get_method(method)
        self.payments = [{
            'amount' : self.amount,
            'tenderType' : 26,
            'note' : charge
        }]
        self.source = util.get_source(source)


    def get_account_id(self, email):
        '''
        Create or update a Neon Account and return the account ID.
        '''
        return Account(email).get_id()


    def get_custom_fields(self, **kwargs):
        '''
        '''
        custom_fields = []

        page = kwargs.get('page')
        if page:
            custom_fields.append(self.format_field('349', page))

        recurring = kwargs.get('recurring')
        if recurring:
            custom_fields.append(self.format_field('358', 'YES'))
            if recurring == 'monthly':
                custom_fields.append(self.format_field('321', '1040', True))
            else:
                custom_fields.append(self.format_field('321', '1095', True))

        referrer = kwargs.get('referrer')
        if referrer:
            custom_fields.append(self.format_field('350', referrer))

        return custom_fields


    def format_field(self, id, value, option=False):
        if option:
            return {'id': id, 'optionValues': [{'id': value}]}
        else:
            return {'id': id, 'value': value}


    def update(self):
        donation = neon.donations.create(
            accountId=self.account_id,
            acknowledgee=self.acknowledgee,
            amount=self.amount,
            anonymousType=self.anonymous,
            campaign=self.campaign,
            date=self.date,
            donationCustomFields=self.custom_fields,
            fund=self.fund,
            payments=self.payments,
            purpose=self.allocation,
            sendAcknowledgeEmail=True,
            solicitationMethod=self.method,
            source=self.source
        )
        print(donation.json())
        return donation.json()
