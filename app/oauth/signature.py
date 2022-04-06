from authlib.jose import JsonWebSignature
from authlib.jose.errors import BadSignatureError
from time import time
from flask import current_app
import json

jws = JsonWebSignature(algorithms=["HS512"])


def get_jws_protected_header(expiration_seconds=None):
    if expiration_seconds:
        # issued at
        iat = int(time())
        exp = iat + expiration_seconds
        protected = {"alg": "HS512", "crit": ["exp"], "iat": iat, "exp": exp}
    else:
        protected = {"alg": "HS512"}
    return protected


def get_jws_token(payload, expiration_seconds=None):
    secret = current_app.config["SECRET_KEY"]
    protected = get_jws_protected_header(expiration_seconds)
    # Specify separators explicitly to remove whitespace.
    payload_str = json.dumps(payload, separators=(",", ":"))
    return jws.serialize_compact(protected, payload_str, secret)


def verify_jws_token(token):
    secret = current_app.config["SECRET_KEY"]

    result = jws.deserialize_compact(token, secret, json.loads)

    # Check expiration if present.
    exp = result.get("header", {}).get("exp")
    if exp and exp <= time():
        raise BadSignatureError("Token expired")

    return result.get("payload")
