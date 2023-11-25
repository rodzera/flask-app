from src.tests.unittests.utils import basic_auth, headers


def test_resource_api_roles_200(client):
    response = client.get(
        "/api/roles", headers=headers(**basic_auth())
    )
    assert response.status_code == 200
    assert response.mimetype == "application/json"


def test_resource_api_roles_401(client):
    response = client.get(
        "/api/roles", headers=headers()
    )
    assert response.status_code == 401
    assert response.mimetype == "application/json"
