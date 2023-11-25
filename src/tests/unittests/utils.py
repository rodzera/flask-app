from typing import Tuple
from base64 import b64encode


def headers(**kwargs):
    return {
        "Accept": "application/json",
        **kwargs
    }


def basic_auth(cred: Tuple = ("admin", "admin")):
    u, p = cred
    credentials = f"{u}:{p}".encode()
    encoded_credentials = b64encode(credentials).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}
