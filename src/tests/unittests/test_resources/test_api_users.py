from unittest.mock import MagicMock

from src.app.models.users import User
from src.tests.unittests.utils import headers, admin_auth, user_auth, \
    mocked_payload

payload = {"name": "test", "users": []}


def test_api_users_get_all_200(client, mocker):
    mocked_model = mocker.patch("src.app.resources.api.users.User")
    mocked_schema = mocker.patch("src.app.resources.api.users.schema")

    mock = MagicMock()
    mocked_model.query.all.return_value = [mock]
    mocked_schema.dump.return_value = mocked_payload

    response = client.get(
        "/api/users", headers=headers(**admin_auth)
    )

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert mocked_payload in response.json["users"]
    mocked_model.query.all.assert_called_once()
    mocked_schema.dump.assert_called_once_with(mock)


def test_api_users_get_by_id_200(client, mocker):
    mocked_db = mocker.patch("src.app.resources.api.users.db")
    mocked_schema = mocker.patch("src.app.resources.api.users.schema")

    query = mocked_db.get_or_404.return_value
    mocked_schema.dump.return_value = mocked_payload

    response = client.get(
        "/api/users/1", headers=headers(**admin_auth)
    )

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == mocked_payload
    mocked_db.get_or_404.assert_called_once_with(User, 1, "User not found")
    mocked_schema.dump.assert_called_once_with(query)


def test_api_users_post_201(client, mocker):
    mocked_schema = mocker.patch("src.app.resources.api.users.schema")

    model = mocked_schema.load.return_value
    mocked_schema.dump.return_value = mocked_payload

    response = client.post(
        "/api/users", headers=headers(**admin_auth), json=payload
    )

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.json == mocked_payload
    mocked_schema.load.assert_called_once_with(payload)
    mocked_schema.dump.assert_called_once_with(model.orm_handler.return_value)
    model.orm_handler.assert_called_once_with("add")


def test_api_users_put_200(client, mocker):
    mocked_db = mocker.patch("src.app.resources.api.users.db")
    mocked_schema = mocker.patch("src.app.resources.api.users.schema")

    query = mocked_db.get_or_404.return_value
    mocked_schema.dump.return_value = mocked_payload

    response = client.put(
        "/api/users/1", json=payload, headers=headers(**admin_auth)
    )

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == mocked_payload
    mocked_db.get_or_404.assert_called_once_with(User, 1, "User not found")
    mocked_schema.load.assert_called_once()
    query.update_attrs.assert_called_once_with(**payload)
    mocked_schema.dump.assert_called_once_with(query.update_attrs.return_value)


def test_api_users_delete_200(client, mocker):
    mocked_db = mocker.patch("src.app.resources.api.users.db")
    mocked_schema = mocker.patch("src.app.resources.api.users.schema")

    query = mocked_db.get_or_404.return_value
    mocked_schema.dump.return_value = mocked_payload

    response = client.delete(
        "/api/users/1", headers=headers(**admin_auth)
    )

    assert response.status_code == 204
    assert response.mimetype == "application/json"
    assert response.get_json(silent=True) is None
    mocked_db.get_or_404.assert_called_once_with(User, 1, "User not found")
    query.orm_handler.assert_called_once_with("delete")


def test_api_users_401(client):
    r1 = client.get("/api/users", headers=headers(**user_auth))
    r2 = client.get("/api/users/1", headers=headers(**user_auth))
    r3 = client.post("/api/users", headers=headers(**user_auth))
    r4 = client.put("/api/users/1", headers=headers(**user_auth))
    r5 = client.delete("/api/users/1", headers=headers(**user_auth))

    assert all(r.status_code == 401 for r in [r1, r2, r3, r4, r5])
    assert all(r.mimetype == "application/json" for r in [r1, r2, r3, r4, r5])
