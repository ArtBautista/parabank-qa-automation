"""Hybrid tests: arrange through the fast REST API, assert in the UI the customer sees."""
from decimal import Decimal
import pytest
from pages import OverviewPage

pytestmark = [pytest.mark.hybrid]

def test_account_created_by_api_appears_in_ui(overview, api, customer):
    """PB-HY-001: an account opened through the API is listed on Accounts Overview."""
    funding = api.accounts(customer["id"])[0]["id"]
    new_account = api.create_account(customer["id"], 1, funding)
    page = OverviewPage(overview.driver).open().wait_until_loaded()
    assert str(new_account["id"]) in page.account_ids()

def test_transfer_by_api_updates_ui_balance(overview, api, two_accounts):
    """PB-HY-002: a transfer made through the API is reflected in the UI balances."""
    from_id, to_id = two_accounts
    before = api.balance(from_id)
    api.transfer(from_id, to_id, "12.34")
    page = OverviewPage(overview.driver).open().wait_until_loaded()
    assert page.balances()[from_id] == before - Decimal("12.34")
