import pytest  # pylint: disable=E0401


def pytest_addoption(parser):
    """
    Adds --base-url and --empty-db options to pytest command line.
    """
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:8000",
        help="Base URL for API tests (e.g., http://localhost:8000)"
    )
    parser.addoption(
        "--db-empty",
        action="store_true",
        default=False,
        help="Run tests for empty DB"
    )


@pytest.fixture(scope="session")
def base_url(request):
    """
    Fixture that provides the base_url from the command line option.
    """
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def db_empty(request):
    """
    Fixture that provides the --db-empty flag value.
    """
    return request.config.getoption("--db-empty")
