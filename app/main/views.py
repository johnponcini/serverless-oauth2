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

import stripe

stripe.api_key =  os.environ.get("STRIPE_SECRET")

main = Blueprint("main", __name__)


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]

"""
@main.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("account.login"))
    return redirect(url_for("main.index"))
"""

@main.route("/", methods=("GET", "POST"))
def home():
    if current_user.is_anonymous:
        return redirect(url_for("account.login"))
    if request.method == "POST":
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(name=username)
            db.session.add(user)
            db.session.commit()
        session["id"] = user.id
        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page)
        return redirect("/")
    user = current_user
    if user:
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
        try:
            customer = stripe.Customer.search(query="email:'{}'".format(user.email))
            customer_id = customer.data[0].id
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=url_for("main.home"),
            )
            portal_url = session.url
        except:
            portal_url = None
    else:
        clients = []

    return render_template("home.html", user=user, clients=clients, portal_url=portal_url)

"""
@main.route("/logout")
def logout():
    del session["id"]
    return redirect("/")
"""

@main.route("/create_client", methods=("GET", "POST"))

def create_client():
    form = RegisterClientForm()
    user = current_user
    if not user:
        return redirect("/")
    if request.method == "GET":
        return render_template("create_client.html")

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
    return redirect("/")


@main.route("/api/me")
@require_oauth("profile")
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)


"""
@main.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("account.login"))
    return redirect(url_for("main.index"))
"""