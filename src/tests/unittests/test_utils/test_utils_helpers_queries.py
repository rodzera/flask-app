from datetime import datetime
from sqlalchemy import Row
from sqlalchemy.exc import OperationalError

from src.app.models.users import User
from src.app.utils.helpers.queries import get_db_timestamp, query_with_entities

mock_datetime = datetime.now()


def test_get_db_timestamp_success(mocker):
    mocked_db = mocker.patch("src.app.utils.helpers.queries.db")
    mocked_text = mocker.patch("src.app.utils.helpers.queries.text")
    mocked_db.engine.connect.return_value.__enter__.return_value.execute.return_value = [[mock_datetime]]

    result = get_db_timestamp()

    assert result == mock_datetime.strftime("%Y-%m-%d %H:%M:%S")
    mocked_text.assert_called_once_with("SELECT CURRENT_TIMESTAMP")
    mocked_db.engine.connect.return_value.__enter__.return_value.execute.assert_called_once_with(mocked_text.return_value)


def test_get_db_timestamp_fail(mocker):
    mocked_db = mocker.patch("src.app.utils.helpers.queries.db")
    mocked_text = mocker.patch("src.app.utils.helpers.queries.text")
    mocked_db.engine.connect.return_value.__enter__.return_value.execute.side_effect = OperationalError("test", "test", BaseException())

    result = get_db_timestamp()

    assert result is False
    mocked_text.assert_called_once_with("SELECT CURRENT_TIMESTAMP")
    mocked_db.engine.connect.return_value.__enter__.return_value.execute.assert_called_once_with(mocked_text.return_value)


def test_query_with_entities(populate_db):
    user = query_with_entities(User, "id", "username", username="user").first()
    assert getattr(user, "username") == "user"

    non_existent_user = query_with_entities(User, "username", username="fake").first()
    assert non_existent_user is None

    users = query_with_entities(User, "id", "username").all()
    assert user in users
    assert all((isinstance(u, Row) and isinstance(u.id, int) and isinstance(u.username, str)) for u in users)

    false = query_with_entities(User)
    assert false is False
