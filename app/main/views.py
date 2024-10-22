import os
import time
from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from flask_login import current_user, login_required

from werkzeug.security import gen_salt
from authlib.integrations.flask_oauth2 import current_token
from app.models import db, User, OAuth2Client
from app.oauth import require_oauth
from app.oauth.forms import RegisterClientForm

from datetime import datetime

import stripe

stripe.api_key =  os.environ.get("STRIPE_SECRET_KEY")
stripe.api_version = "2020-08-27"

main = Blueprint("main", __name__)


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]


@main.route("/", methods=("GET", "POST"))
def home():
    if current_user.is_anonymous:
        return redirect(url_for("account.login"))

    
    if request.method == "POST":
        '''
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(name=username)
            db.session.add(user)
            db.session.commit()
        session["id"] = user.id
        # if user is not just to log in, but need to head back to the auth page, then go for it
        '''
        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page)
        return redirect("/")

    user = current_user
    if user:
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()

        # Search for an existing Stripe customer 
        try:
            customer = stripe.Customer.search(query="email:'{}'".format(user.email))
            customer_id = customer.data[0].id
            session['customer'] = customer_id
        except:
            customer_id = None
        # Create a new customer if one does not already exist
        if not customer_id:
            customer = stripe.Customer.create(email=user.email, name=user.name)
            customer_id = customer.id

        portal = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=request.base_url,
        )
        session['portal'] = portal.url

        subscriptions = stripe.Subscription.list(customer=customer_id)
        charges = stripe.Charge.list(customer=customer_id, limit=25)
        donations = []
        for charge in charges.data:
            if charge['paid']:
                amount = charge['amount']
                date = datetime.utcfromtimestamp(charge['created']).strftime('%Y-%m-%d')
                donations.append((amount, date))
        
    else:
        subscriptions=None
        donations=None
        clients = []

    if current_user.role_id == 1:
        admin = True
    else:
        admin = False

    return render_template(
        "home.html", 
        user=user, 
        clients=clients, 
        portal_url=session.get('portal'), 
        subscriptions=subscriptions, 
        donations=donations, 
        admin=admin
    )



@main.route("/create_client", methods=("GET", "POST"))
def create_client():
    form = RegisterClientForm()
    user = current_user
    if not user:
        return redirect("/")
    if request.method == "GET":
        return render_template("create_client.html", form=form)

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user.id,
    )

    client_metadata = {
        "client_name": form.client_name.data,
        "client_uri": form.client_uri.data,
        "grant_types": split_by_crlf(form.grant_type.data),
        "redirect_uris": split_by_crlf(form.redirect_uri.data),
        "response_types": split_by_crlf(form.response_type.data),
        "scope": form.scope.data,
        "token_endpoint_auth_method": form.token_endpoint_auth_method.data,
    }
    client.set_client_metadata(client_metadata)

    if form["token_endpoint_auth_method"] == "none":
        client.client_secret = ""
    else:
        client.client_secret = gen_salt(48)

    db.session.add(client)
    db.session.commit()
    return redirect(url_for('.home'))


@main.route("/api/me")
@require_oauth("profile")
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.email)

"""
@main.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("account.login"))
    return redirect(url_for("main.index"))
"""