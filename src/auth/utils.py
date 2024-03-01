"""Contains utility functions for the auth module."""


from datetime import datetime, timedelta
from uuid import uuid4
from os import getenv
from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def create_token(payload: dict) -> str:
    """Creates a JWT token from a payload."""
    payload["exp"] = datetime.utcnow() + timedelta(days=7)
    payload["iat"] = datetime.utcnow()
    payload["jti"] = str(uuid4())
    payload['iss'] = 'AASTU-SpaceWiki'
    token = encode(payload=payload,
                   key=getenv("JWT_SECRET"),
                   algorithm="HS256")
    return token


def decode_token(token: str) -> dict:
    """Decodes a JWT token."""
    try:
        payload = decode(token, key=getenv("JWT_SECRET"), algorithms=["HS256"])
        return {"username": payload['username']}
    except ExpiredSignatureError:
        return {"error": "Token expired."}
    except InvalidTokenError:
        return {"error": "Invalid token."}
    except Exception:
        return {"error": "Error decoding the token."}
