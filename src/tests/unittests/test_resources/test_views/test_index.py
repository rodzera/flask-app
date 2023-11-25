def test_resource_views_index(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert response.request.path == "/apidocs/"
