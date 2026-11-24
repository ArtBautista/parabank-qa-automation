import pytest
from config import PASSWORD, USERNAME
from pages import LoginPage


NOT_VERIFIED = "The username and password could not be verified."
EMPTY = "Please enter a username and password."


@pytest.mark.smoke
def test_valid_login_opens_accounts_overview(driver, customer):
    """PB-UI-001: valid credentials open Accounts Overview with a welcome message."""
    overview = LoginPage(driver).open().login(USERNAME, PASSWORD)

    assert overview.heading == "Accounts Overview"
    assert overview.welcome_text() == f"Welcome {customer['firstName']} {customer['lastName']}"
    assert len(overview.account_ids()) >= 1

@pytest.mark.negative
@pytest.mark.parametrize(
    "username, password, expected",
    [
        (USERNAME, "wrong-password-123", NOT_VERIFIED),
        ("no_such_user_xyz", "whatever", NOT_VERIFIED),
        ("", "", EMPTY),
    ],
    ids=["PB-UI-002-wrong-password", "PB-UI-003-unknown-user", "PB-UI-004-empty"],
)

def test_invalid_login_shows_error(driver, username, password, expected):
    """PB-UI-002 to 004: invalid credentials show an error and no account menu."""
    page = LoginPage(driver).open()
    page.submit_credentials(username, password)
    assert page.error_message() == expected
    assert not page.is_visible(page.LOG_OUT, timeout=1)

def test_log_out_returns_to_login(overview):
    """PB-UI-005: Log Out ends the session and shows the login form again."""
    overview.log_out()
    page = LoginPage(overview.driver)
    assert page.is_visible(page.USERNAME)
    assert not page.is_visible(page.LOG_OUT, timeout=1)
