import pytest
from pages import BillPayPage
PAYEE = {
    "name": "Meralco", "street": "Ortigas Ave", "city": "Pasig", "state": "NCR",
    "zip_code": "1600", "phone": "0281234567", "account": "54321", "verify_account": "54321",
}

@pytest.mark.smoke
def test_bill_payment_succeeds(overview, api, customer):
    """PB-UI-040: a valid bill payment shows a confirmation naming the payee."""
    page = BillPayPage(overview.driver).open()
    page.pay(**PAYEE, amount="15")
    assert page.heading == "Bill Payment Complete"
    assert page.text_of(page.RESULT_PAYEE) == PAYEE["name"]

@pytest.mark.negative
def test_bill_pay_account_mismatch(overview):
    """PB-UI-041: different account and verify-account numbers are rejected."""
    page = BillPayPage(overview.driver).open()
    page.fill(**{**PAYEE, "verify_account": "99999"}, amount="15")
    page.submit()
    assert page.error("verify_mismatch") == "The account numbers do not match."

@pytest.mark.negative
def test_bill_pay_required_fields(overview):
    """PB-UI-042: submitting an empty form shows the required-field errors."""
    page = BillPayPage(overview.driver).open()
    page.wait_for_options(page.FROM_ACCOUNT)
    page.submit()
    assert page.error("name") == "Payee name is required."
    assert page.error("amount") == "The amount cannot be empty."
