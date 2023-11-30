from src.app.utils import jsonify_success_response, jsonify_error_response


def test_jsonify_success_response(mocker):
    mocked_make_resp = mocker.patch("src.app.utils.helpers.json.make_response")
    response = jsonify_success_response(status_code=201)

    assert response == mocked_make_resp.return_value
    assert mocked_make_resp.return_value.status == 201
    mocked_make_resp.assert_called_once_with({"status": "success"})


def test_jsonify_error_response(mocker):
    mocked_make_resp = mocker.patch("src.app.utils.helpers.json.make_response")
    response = jsonify_error_response(500, "error", "message")

    assert response == mocked_make_resp.return_value
    assert mocked_make_resp.return_value.status == 500
    mocked_make_resp.assert_called_once_with({"status_code": 500, "name": "error", "message": "message"})
