def test_populate_roles_command(mocker, runner):
    mocked_cls = mocker.patch("src.app.utils.cli_commands.Role")
    runner.invoke(args="populate_roles")
    mocked_cls.create_default_roles.assert_called_once()
