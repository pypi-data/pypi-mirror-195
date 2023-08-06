import pytest

W_INT_CLI_FLAG = "--with-integration"
O_INT_CLI_FLAG = "--only-integration"
W_S_INT_CLI_FLAG = "--with-slow-integration"
O_S_INT_CLI_FLAG = "--only-slow-integration"

INT_MARKER = "integration"
S_INT_MARKER = "slow_integration"


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        f"{INT_MARKER}: mark tests as integration tests and only run when "
        f"{W_INT_CLI_FLAG} or {O_INT_CLI_FLAG} is passed",
    )
    config.addinivalue_line(
        "markers",
        f"{S_INT_MARKER}: mark tests as slow integration tests and only run when "
        f"{W_S_INT_CLI_FLAG} or {O_S_INT_CLI_FLAG} is passed",
    )


def pytest_addoption(parser):
    group = parser.getgroup("pytest-extra-markers")
    group.addoption(W_INT_CLI_FLAG, action="store_true", help="Run integration tests")
    group.addoption(
        O_INT_CLI_FLAG, action="store_true", help="Only run integration tests"
    )
    group.addoption(
        W_S_INT_CLI_FLAG, action="store_true", help="Run slow integration tests"
    )
    group.addoption(
        O_S_INT_CLI_FLAG, action="store_true", help="Only slow integration tests"
    )


def pytest_collection_modifyitems(config, items):
    w_int = config.getoption(W_INT_CLI_FLAG)
    o_int = config.getoption(O_INT_CLI_FLAG)
    w_s_int = config.getoption(W_S_INT_CLI_FLAG)
    o_s_int = config.getoption(O_S_INT_CLI_FLAG)

    skip_integration = pytest.mark.skip(reason="Integration tests are being skipped")
    skip_non_integration = pytest.mark.skip(
        reason="Non-integration tests are being skipped"
    )
    skip_s_integration = pytest.mark.skip(
        reason="Slow integration tests are being skipped"
    )
    skip_non_s_integration = pytest.mark.skip(
        reason="Non-slow integration tests are being skipped"
    )

    if w_int and w_s_int:
        return

    if o_s_int and o_int:
        raise Exception(f"Cannot have both {O_INT_CLI_FLAG} and {O_S_INT_CLI_FLAG}")

    for item in items:
        int_in_kw = INT_MARKER in item.keywords
        s_int_in_kw = S_INT_MARKER in item.keywords
        apply = []

        if o_int:
            if not int_in_kw:
                apply.append(skip_non_integration)
        elif o_s_int:
            if not s_int_in_kw:
                apply.append(skip_non_s_integration)
        elif w_int:
            if s_int_in_kw:
                apply.append(skip_s_integration)
        elif w_s_int:
            if int_in_kw:
                apply.append(skip_integration)
        else:
            if int_in_kw:
                apply.append(skip_integration)
            if s_int_in_kw:
                apply.append(skip_s_integration)

        for marker in apply:
            item.add_marker(marker)
