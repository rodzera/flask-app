from unittest.mock import call


def test_populate_roles_command(mocker, runner):
    mocked_model = mocker.patch("src.app.utils.cli_commands.Role")
    mocked_model.query.filter_by.return_value.first.return_value = None

    runner.invoke(args="populate_roles")

    mocked_model.query.filter_by.assert_has_calls(
        [call(name="admin"), call().first(), call(name="user"), call().first()]
    )
    mocked_model.assert_has_calls(
        [call(name="admin"), call(name="user")],
        any_order=True
    )
    mocked_model.return_value.orm_handler.assert_has_calls(
        [call("add"), call("add")]
    )
