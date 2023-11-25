from src.tests.unittests.utils import basic_auth, headers


def test_resource_api_users_200(client):
    response = client.get(
        "/api/users",
        headers=headers(**basic_auth())
    )
    assert response.status_code == 200
    assert response.mimetype == "application/json"


def test_resource_api_users_401(client):
    response = client.get("/api/users", headers=headers())
    assert response.status_code == 401
    assert response.mimetype == "application/json"
