from datetime import datetime
from src.app.constants import VERSION
from src.tests.unittests.utils import headers


def test_resource_api_database_up(client, mocker):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mocked_f = mocker.patch("src.app.resources.api.status.get_db_timestamp", return_value=dt)
    response = client.get("/api/database", headers=headers())
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == {"status": "up", "datetime": dt}
    assert mocked_f.called_once()


def test_resource_api_database_down(client, mocker):
    mocked_f = mocker.patch("src.app.resources.api.status.get_db_timestamp", return_value=False)
    response = client.get("/api/database", headers=headers())
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == {"status": "down"}
    assert mocked_f.called_once()


def test_resource_api_server_up(client):
    response = client.get("/api/server", headers=headers())
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == {"status": "up", **VERSION}
