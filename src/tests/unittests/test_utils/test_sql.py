from datetime import datetime
from sqlalchemy.exc import OperationalError

from src.app.utils.sql import get_db_timestamp

mock_datetime = datetime.now()


def test_utils_sql_get_db_timestamp_success(mocker):
    mocked_db = mocker.patch("src.app.utils.sql.db")
    mocked_text = mocker.patch("src.app.utils.sql.text")
    mocked_db.engine.connect.return_value.__enter__.return_value.execute.return_value = [[mock_datetime]]

    result = get_db_timestamp()

    assert result == mock_datetime.strftime("%Y-%m-%d %H:%M:%S")
    mocked_text.assert_called_once_with("SELECT CURRENT_TIMESTAMP")
    mocked_db.engine.connect.return_value.__enter__.return_value.execute.assert_called_once_with(mocked_text.return_value)


def test_utils_sql_get_db_timestamp_fail(mocker):
    mocked_db = mocker.patch("src.app.utils.sql.db")
    mocked_text = mocker.patch("src.app.utils.sql.text")
    mocked_db.engine.connect.return_value.__enter__.return_value.execute.side_effect = OperationalError("test", "test", BaseException())

    result = get_db_timestamp()

    assert result is False
    mocked_text.assert_called_once_with("SELECT CURRENT_TIMESTAMP")
    mocked_db.engine.connect.return_value.__enter__.return_value.execute.assert_called_once_with(mocked_text.return_value)
