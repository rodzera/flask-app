from src.tests.unittests.utils import basic_auth, headers

payload = {"level": "INFO"}


def test_resource_api_settings_logs_get_200(client):
    response = client.get(
        "/api/settings/logs",
        headers=headers(**basic_auth())
    )
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == payload


def test_resource_api_settings_logs_put_200(client, mocker):
    mocked_schema = mocker.patch("src.app.resources.api.settings.LoggerLevelSchema")
    response = client.put(
        "/api/settings/logs",
        json=payload,
        headers=headers(**basic_auth())
    )
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == payload
    assert mocked_schema.called_once_with(payload)


def test_resource_api_settings_logs_401(client):
    r1 = client.get("/api/settings/logs", headers=headers())
    r2 = client.put(
        "/api/settings/logs",
        json=payload,
        headers=headers()
    )
    assert all(r.status_code == 401 for r in [r1, r2])
    assert all(r.mimetype == "application/json" for r in [r1, r2])
