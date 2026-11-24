import pytest
from pages import RegisterPage

VALID = {
    "first_name": "Ana", "last_name": "Cruz", "street": "1 Test St", "city": "Manila",
    "state": "NCR", "zip_code": "1000", "phone": "09170000000", "ssn": "123-45-6789",
}

@pytest.mark.smoke
def test_register_new_customer(driver, unique_username):
    """PB-UI-010: a new customer can register and is signed in straight away."""
    page = RegisterPage(driver).open()
    page.register(**VALID, username=unique_username, password="Secret#123", confirm="Secret#123")
    assert page.heading == f"Welcome {unique_username}"
    assert "Your account was created successfully" in page.text_of(page.SUCCESS_TEXT)
    assert page.welcome_text() == f"Welcome {VALID['first_name']} {VALID['last_name']}"

@pytest.mark.negative
def test_register_password_mismatch(driver, unique_username):
    """PB-UI-011: different password and confirmation are rejected."""
    page = RegisterPage(driver).open()
    page.register(**VALID, username=unique_username, password="Secret#123", confirm="Other#456")
    assert page.error_for("confirm") == "Passwords did not match."

@pytest.mark.negative
def test_register_duplicate_username(driver, unique_username):
    """PB-UI-012: a username can only be registered once."""
    first = RegisterPage(driver).open()
    first.register(**VALID, username=unique_username, password="Secret#123", confirm="Secret#123")
    first.log_out()
    second = RegisterPage(driver).open()
    second.register(**VALID, username=unique_username, password="Secret#123", confirm="Secret#123")
    assert second.error_for("username") == "This username already exists."

@pytest.mark.negative
@pytest.mark.parametrize(
    "key, message",
    [("first_name", "First name is required."), ("ssn", "Social Security Number is required.")],
    ids=["PB-UI-013-first-name", "PB-UI-014-ssn"],
)

def test_register_required_fields(driver, unique_username, key, message):
    """PB-UI-013 to 014: leaving a required field empty shows its error."""
    values = {**VALID, "username": unique_username, "password": "Secret#123",
    "confirm": "Secret#123"}
    values.pop(key)

    page = RegisterPage(driver).open()

    page.register(**values)

    assert page.error_for(key) == message
