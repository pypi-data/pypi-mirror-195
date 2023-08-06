from unittest.mock import patch

from click.testing import CliRunner

from blazetest.core.project_config.project_config import ProjectConfiguration
from blazetest.runner import run_tests


@patch("blazetest.runner.TestsRunnerFacade")
@patch("blazetest.runner.LicenseManager.check_license")
@patch("blazetest.runner.PulumiManager.deploy")
def test_tests_runner(deploy_mock, check_license_mock, tests_runner_facade):
    deploy_mock.return_value = None
    check_license_mock.return_value = "21 Jun 2028"
    tests_runner_facade.run_tests.return_value = None

    runner = CliRunner()
    result = runner.invoke(
        run_tests,
        [
            "-v",
            "--config-path",
            "tests/core/test_config/config1.yaml",
            "--license-key",
            "test-key",
        ],
    )

    config = ProjectConfiguration.from_yaml("tests/core/test_config/config1.yaml")
    assert result.exit_code == 0
    tests_runner_facade.assert_called_with(
        pytest_args=["-v"],
        config=config,
    )

    result = runner.invoke(
        run_tests,
        [
            "-v",
            "--config-path=tests/core/test_config/config1.yaml",
            "--license-key=test-key",
        ],
    )

    assert result.exit_code == 0
    tests_runner_facade.assert_called_with(pytest_args=["-v"], config=config)
