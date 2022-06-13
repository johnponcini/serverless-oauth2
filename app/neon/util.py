from iso3166 import countries
from app.neon import neon

COUNTRIES = neon.properties.get_countries().json()

SOURCES = {
#this allows us to map each donation page to a different source in Neon
    'https://maps.org/donate' : {'id' : 859},
    'https://www.maps.org/' : {'id' : 860},
    'https://maps.org/' : {'id' : 860},
    '3RD PARTY - Funraise' : {'id' : 843},
    'https://maps.org/jennandnayel' : {'id' : 902},
    'https://maps.org/join' : {'id' : 904},
    'development-event' : {'id' : 787},
    'Stripe Checkout' : {'id' : 910},
    'MAPSi' : {'id' : 921}
}

METHODS = {
    'online' : {'id' : 14},
    'mailer' : {'id' : 2},
    'email' : {'id' : 4},
    'social' : {'id' : 5},
    'unknown' : {'id' : 13},
    'ad' : {'id' : 15}
}

ALLOCATIONS = {
    'unrestricted' : {'id' : 1},
    'phase 3' : {'id' : 324},
    'health-equity' : {'id': 381}
}

CAMPAIGNS = {
    'general support' : {'id' : 11},
    'capstone' : {'id' : 189},
    '35th' : {'id' : 207},
    '214 - wedding' : {'id' : 214},
    '216 - team psychedelics' : {'id' : 216},
    'austin2021' : {'id' : 221},
    'capstone challenge' : {'id' : 189},
    'year-end2021' : {'id' : 225},
    'health-equity' : {'id' : 194}
}

def get_country_id(country):
    '''
    '''
    name = countries.get(country).name
    return next((x for x in COUNTRIES if x['name'] == name), None)

def get_campaign(campaign):
    try:
        return CAMPAIGNS[campaign]
    except:
        return {'id' : 11}

def get_method(method):
    try:
        return METHODS[method]
    except:
        return {'id' : 14}

def get_allocation(allocation):
    try:
        return ALLOCATIONS[allocation]
    except:
        return {'id' : 1}

def get_source(source):
    try:
        return SOURCES[source]
    except:
        return {'id' : 910}

def add_bulletin_fields(address):
    return [
        {
            'id': '330',
            'name': 'Bulletin Address 1',
            'value': address['line1']
        },
        {
            'id': '331',
            'name': 'Bulletin Address 2',
            'value': address['line2']
        },
        {
            'id': '332',
            'name': 'Bulletin City',
            'value': address['city']
        },
        {
            'id': '335',
            'name': 'Bulletin Country',
            'value': address['country']
        },
        {
            'id': '334',
            'name': 'Bulletin Postal Code',
            'value': address['postal_code']
        }
    ]

def email_admin():
    pass
