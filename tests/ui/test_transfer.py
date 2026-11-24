from decimal import Decimal

import pytest

from pages import TransferPage


@pytest.mark.smoke
def test_transfer_moves_money(overview, api, two_accounts):
    """PB-UI-030: a transfer shows a confirmation and moves the exact amount."""
    from_id, to_id = two_accounts
    before_from, before_to = api.balance(from_id), api.balance(to_id)
    page = TransferPage(overview.driver).open()

    page.transfer("25.50", from_id, to_id)

    assert page.heading == "Transfer Complete!"
    assert page.text_of(page.RESULT_FROM) == from_id
    assert page.text_of(page.RESULT_TO) == to_id
    assert api.balance(from_id) == before_from - Decimal("25.50")
    assert api.balance(to_id) == before_to + Decimal("25.50")


@pytest.mark.negative
@pytest.mark.xfail(
    reason="DEF-002: invalid amount shows 'An internal error has occurred' "
           "instead of a validation message",
    strict=True,
)
@pytest.mark.parametrize(
    "amount, message",
    [("", "The amount cannot be empty."), ("abc", "Please enter a valid amount.")],
    ids=["PB-UI-031-empty", "PB-UI-032-not-a-number"],
)
def test_transfer_amount_validation(overview, two_accounts, amount, message):
    """PB-UI-031 to 032: an empty or non-numeric amount is rejected on the page."""
    from_id, to_id = two_accounts
    page = TransferPage(overview.driver).open()

    page.fill(amount, from_id, to_id)
    page.click(page.SUBMIT)

    assert page.visible_amount_error() == message
    assert not page.is_visible(page.RESULT, timeout=1)
