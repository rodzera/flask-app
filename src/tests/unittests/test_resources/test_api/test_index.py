def test_index_api(client):
    response = client.get("/api", follow_redirects=True)
    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert response.request.path == "/apidocs/"
