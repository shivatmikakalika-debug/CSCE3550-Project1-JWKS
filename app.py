
import base64
import time
import uuid

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import Flask, jsonify, request

app = Flask(__name__)


# Generate an RSA key pair with a unique ID and expiry time.
def generate_key(expired=False):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    return {
        "private_key": private_key,
        "kid": str(uuid.uuid4()),
        "expiry": int(time.time()) + (-3600 if expired else 3600),
    }


# Create one valid key and one expired key.
valid_key = generate_key()
expired_key = generate_key(expired=True)


# Convert an integer to Base64URL format for a JWK.
def base64url(number):
    data = number.to_bytes(
        (number.bit_length() + 7) // 8,
        byteorder="big",
    )
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


# Convert an RSA public key into JWK format.
def create_jwk(key):
    public_numbers = key["private_key"].public_key().public_numbers()

    return {
        "kty": "RSA",
        "kid": key["kid"],
        "use": "sig",
        "alg": "RS256",
        "n": base64url(public_numbers.n),
        "e": base64url(public_numbers.e),
    }


# Serve only public keys that have not expired.
@app.route("/.well-known/jwks.json", methods=["GET"])
def jwks():
    keys = [valid_key, expired_key]

    public_keys = [
        create_jwk(key)
        for key in keys
        if key["expiry"] > time.time()
    ]

    return jsonify({"keys": public_keys})


# Issue a signed JWT for a mock user.
@app.route("/auth", methods=["POST"])
def auth():
    is_expired = "expired" in request.args

    key = expired_key if is_expired else valid_key

    current_time = int(time.time())

    payload = {
        "sub": "fake-user",
        "iat": current_time,
        "exp": (
            key["expiry"]
            if is_expired
            else current_time + 3600
        ),
    }

    token = jwt.encode(
        payload,
        key["private_key"],
        algorithm="RS256",
        headers={"kid": key["kid"]},
    )

    return token, 200, {"Content-Type": "text/plain"}


# Start the web server on port 8080.
if __name__ == "__main__":
    app.run(port=8080)