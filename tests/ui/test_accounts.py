import pytest
from pages import CHECKING, SAVINGS, OpenAccountPage

@pytest.mark.smoke
def test_overview_matches_api(overview, api, customer):
    """PB-UI-020: every account and balance on the overview matches the REST API."""
    expected = {str(a["id"]): api.balance(a["id"]) for a in api.accounts(customer["id"])}
    assert overview.balances() == expected

@pytest.mark.parametrize("account_type, type_name", [(SAVINGS, "SAVINGS"), (CHECKING, "CHECKING")],
                        ids=["PB-UI-021-savings", "PB-UI-022-checking"])
def test_open_new_account(overview, api, account_type, type_name):
    """PB-UI-021 to 022: opening an account shows its number; the API confirms its type."""
    page = OpenAccountPage(overview.driver).open()
    new_id = page.open_account(account_type)
    assert new_id.isdigit()
    assert api.account(new_id)["type"] == type_name
