from src.app.constants import ABOUT
from src.tests.unittests.utils import headers


def test_resource_api_about(client):
    response = client.get("/api/about", headers=headers())
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == ABOUT
