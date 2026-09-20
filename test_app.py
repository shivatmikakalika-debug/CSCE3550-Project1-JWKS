
import time

import jwt
import pytest

from app import (
    app,
    base64url,
    create_jwk,
    expired_key,
    generate_key,
    valid_key,
)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_jwks_endpoint(client):
    response = client.get("/.well-known/jwks.json")

    assert response.status_code == 200
    assert "keys" in response.json


def test_valid_key_in_jwks(client):
    response = client.get("/.well-known/jwks.json")

    kids = [key["kid"] for key in response.json["keys"]]

    assert valid_key["kid"] in kids


def test_expired_key_not_in_jwks(client):
    response = client.get("/.well-known/jwks.json")

    kids = [key["kid"] for key in response.json["keys"]]

    assert expired_key["kid"] not in kids


def test_jwk_format():
    jwk = create_jwk(valid_key)

    assert jwk["kty"] == "RSA"
    assert jwk["alg"] == "RS256"
    assert jwk["use"] == "sig"
    assert jwk["kid"] == valid_key["kid"]
    assert "n" in jwk
    assert "e" in jwk


def test_valid_auth(client):
    response = client.post("/auth")

    assert response.status_code == 200

    token = response.data.decode()

    header = jwt.get_unverified_header(token)

    assert header["kid"] == valid_key["kid"]

    payload = jwt.decode(
        token,
        valid_key["private_key"].public_key(),
        algorithms=["RS256"],
    )

    assert payload["exp"] > time.time()


def test_expired_auth(client):
    response = client.post("/auth?expired")

    assert response.status_code == 200

    token = response.data.decode()

    header = jwt.get_unverified_header(token)

    assert header["kid"] == expired_key["kid"]

    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(
            token,
            expired_key["private_key"].public_key(),
            algorithms=["RS256"],
        )


def test_get_auth_not_allowed(client):
    response = client.get("/auth")

    assert response.status_code == 405


def test_post_jwks_not_allowed(client):
    response = client.post("/.well-known/jwks.json")

    assert response.status_code == 405


def test_generate_valid_key():
    key = generate_key()

    assert key["expiry"] > time.time()
    assert key["kid"]
    assert key["private_key"]


def test_generate_expired_key():
    key = generate_key(expired=True)

    assert key["expiry"] < time.time()


def test_unique_kids():
    first = generate_key()
    second = generate_key()

    assert first["kid"] != second["kid"]


def test_base64url():
    result = base64url(65537)

    assert result == "AQAB"