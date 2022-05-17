from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from config import csrf

from authlib.oauth2 import OAuth2Error, OAuth2Request
from app.oauth import authorization
from app.account.views import User
from app.oauth.forms import AuthorizeConsentForm


oauth = Blueprint("oauth", __name__)


@oauth.route("/authorize", methods=["GET", "POST"])
@csrf.exempt
def authorize():
    form = AuthorizeConsentForm()
    # if user log status is not true (Auth server), then to log it in
    if current_user.is_anonymous:
        return redirect(url_for("account.login", next=request.url))
    if request.method == "GET":
        grant = authorization.get_consent_grant(end_user=current_user)
        #client = grant.client
        #scope = client.get_allowed_scope(grant.request.scope)
        
        return render_template(
            "authorize.html", 
            user=current_user,
            grant=grant,
            form=form
            )
        
    if form.confirm.data:
        grant_user = current_user
    else:
        grant_user = None

    return authorization.create_authorization_response(request=request, grant_user=grant_user)


@oauth.route("/token", methods=["POST"])
@csrf.exempt
def issue_token():
    return authorization.create_token_response(request=request)


@oauth.route("/revoke", methods=["POST"])
@csrf.exempt
def revoke_token():
    return authorization.create_endpoint_response("revocation")
