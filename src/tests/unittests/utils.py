from base64 import b64encode


def headers(**kwargs):
    return {
        "Accept": "application/json",
        **kwargs
    }


def basic_auth(username: str, password: str):
    credentials = f"{username}:{password}".encode()
    encoded_credentials = b64encode(credentials).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}


mocked_response = {"test": "test"}
admin_auth = basic_auth("admin", "admin")
user_auth = basic_auth("user", "user")
