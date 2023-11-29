from src.tests.unittests.utils import headers, admin_auth, user_auth

payload = {"level": "INFO"}


def test_resource_api_settings_logs_get_200(client):
    response = client.get("/api/settings/logs", headers=headers(**admin_auth))
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == payload


def test_resource_api_settings_logs_put_200(client, mocker):
    mocked_schema = mocker.patch("src.app.resources.api.settings.schema")
    response = client.put(
        "/api/settings/logs", json=payload, headers=headers(**admin_auth)
    )
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == payload
    mocked_schema.load.assert_called_once_with(payload)


def test_resource_api_settings_logs_401(client):
    r1 = client.get("/api/settings/logs", headers=headers())
    r2 = client.put(
        "/api/settings/logs", json=payload, headers=headers(**user_auth)
    )
    assert all(r.status_code == 401 for r in [r1, r2])
    assert all(r.mimetype == "application/json" for r in [r1, r2])
