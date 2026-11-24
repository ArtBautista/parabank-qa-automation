import pytest

from pages import FindTransactionsPage, RequestLoanPage, TransferPage


def richest_account(api, customer):
    """Account id with the highest balance, so the down payment is affordable."""
    return str(max(api.accounts(customer["id"]), key=lambda a: a["balance"])["id"])


def test_small_loan_is_approved(overview, api, customer):
    """PB-UI-050: a small loan with a small down payment is approved."""
    page = RequestLoanPage(overview.driver).open()

    status = page.apply(amount="100", down_payment="10",
                        from_account_id=richest_account(api, customer))

    assert status == "Approved"
    assert page.text_of(page.NEW_ACCOUNT_ID).isdigit()


@pytest.mark.negative
def test_huge_loan_is_denied(overview, api, customer):
    """PB-UI-051: a loan far above the customer's funds is denied with a reason."""
    page = RequestLoanPage(overview.driver).open()

    status = page.apply(amount="99999999", down_payment="10",
                        from_account_id=richest_account(api, customer))

    assert status == "Denied"
    assert page.denial_message().startswith("We cannot grant a loan in that amount")


def test_find_transaction_by_amount(overview, two_accounts):
    """PB-UI-060: a transfer can be found again by its amount."""
    from_id, to_id = two_accounts
    TransferPage(overview.driver).open().transfer("7.77", from_id, to_id)
    page = FindTransactionsPage(overview.driver).open()

    page.find_by_amount(from_id, "7.77")

    assert page.result_count() >= 1


@pytest.mark.negative
def test_find_transaction_invalid_id(overview, two_accounts):
    """PB-UI-061: a non-numeric transaction id shows a validation error."""
    from_id, _ = two_accounts
    page = FindTransactionsPage(overview.driver).open()

    page.submit_transaction_id(from_id, "abc")

    assert page.text_of(page.TRANSACTION_ID_ERROR) == "Invalid transaction ID"
