from src.tests.unittests.utils import headers, admin_auth, user_auth


def test_resource_api_users_200(client):
    response = client.get("/api/users", headers=headers(**admin_auth))
    assert response.status_code == 200
    assert response.mimetype == "application/json"


def test_resource_api_users_401(client):
    response = client.get("/api/users", headers=headers(**user_auth))
    assert response.status_code == 401
    assert response.mimetype == "application/json"
