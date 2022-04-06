from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from authlib.oauth2 import OAuth2Error
from app.account.views import User
from app.oauth import authorization

oauth = Blueprint("oauth", __name__)


@oauth.route("/authorize", methods=["GET", "POST"])
def authorize():
    user = current_user()
    # if user log status is not true (Auth server), then to log it in
    if not user:
        return redirect(url_for("website.routes.home", next=request.url))
    if request.method == "GET":
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template("authorize.html", user=user, grant=grant)
    if not user and "username" in request.form:
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
    if request.form["confirm"]:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)


@oauth.route("/token", methods=["POST"])
def issue_token():
    return authorization.create_token_response()


@oauth.route("/revoke", methods=["POST"])
def revoke_token():
    return authorization.create_endpoint_response("revocation")
