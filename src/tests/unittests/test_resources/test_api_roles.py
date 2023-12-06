from src.tests.unittests.utils import headers, admin_auth, user_auth, payload


def test_api_roles_get_all_200(client, mocker):
    mocked_cls = mocker.patch("src.app.resources.api.roles.Role")
    mocked_cls.dump_all.return_value = [payload]

    response = client.get(
        "/api/roles", headers=headers(**admin_auth)
    )

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert payload in response.json["roles"]
    mocked_cls.dump_all.assert_called_once()


def test_api_roles_get_by_id_200(client, mocker):
    mocked_cls = mocker.patch("src.app.resources.api.roles.Role")
    mocked_cls.dump.return_value = payload

    response = client.get(
        "/api/roles/1", headers=headers(**admin_auth)
    )

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == payload
    mocked_cls.dump.assert_called_once_with(1)


def test_api_roles_post_201(client, mocker):
    mocked_cls = mocker.patch("src.app.resources.api.roles.Role")
    mocked_cls.load.return_value.self_dump.return_value = payload

    response = client.post(
        "/api/roles", headers=headers(**admin_auth), json=payload
    )

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.json == payload
    mocked_cls.load.assert_called_once_with(**payload)
    mocked_cls.load.return_value.self_dump.assert_called_once_with()


def test_api_roles_put_200(client, mocker):
    mocked_cls = mocker.patch("src.app.resources.api.roles.Role")
    mocked_cls.update.return_value.self_dump.return_value = payload

    response = client.put(
        "/api/roles/1", json=payload, headers=headers(**admin_auth)
    )

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == payload
    mocked_cls.update.assert_called_once_with(1, **payload)
    mocked_cls.update.return_value.self_dump.assert_called_once_with()


def test_api_roles_delete_200(client, mocker):
    mocked_cls = mocker.patch("src.app.resources.api.roles.Role")
    mocked_cls.delete.return_value = {}

    response = client.delete(
        "/api/roles/1", headers=headers(**admin_auth)
    )

    assert response.status_code == 204
    assert response.mimetype == "application/json"
    assert response.get_json(silent=True) is None
    mocked_cls.delete.assert_called_once_with(1)


def test_api_roles_401(client):
    r1 = client.get("/api/roles", headers=headers(**user_auth))
    r2 = client.get("/api/roles/1", headers=headers(**user_auth))
    r3 = client.post("/api/roles", headers=headers(**user_auth))
    r4 = client.put("/api/roles/1", headers=headers(**user_auth))
    r5 = client.delete("/api/roles/1", headers=headers(**user_auth))

    assert all(r.status_code == 401 for r in [r1, r2, r3, r4, r5])
    assert all(r.mimetype == "application/json" for r in [r1, r2, r3, r4, r5])
