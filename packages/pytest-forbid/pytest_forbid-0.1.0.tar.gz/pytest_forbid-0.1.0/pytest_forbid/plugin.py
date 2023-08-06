from typing import Iterator

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from forbid.contrib.requests import forbid_requests


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--forbid-requests",
        action="store_true",
        dest="requests_forbidden",
        help="Forbid any calls to requests package.",
    )


@pytest.fixture(autouse=True)
def _forbid_requests(request: SubRequest) -> Iterator[None]:
    requests_forbidden = request.config.getoption("requests_forbidden")

    if requests_forbidden:
        with forbid_requests():
            yield
    else:
        yield
