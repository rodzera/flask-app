def test_populate_roles_command(mocker, runner):
    mocked_function = mocker.patch("src.app.utils.cli_commands.create_default_roles")
    runner.invoke(args="populate_roles")
    mocked_function.assert_called_once()
