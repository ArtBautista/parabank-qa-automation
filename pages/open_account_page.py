"""Open New Account: choose CHECKING or SAVINGS and a funding account."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

CHECKING, SAVINGS = "0", "1"

class OpenAccountPage(BasePage):

    path = "/openaccount.htm"
    TYPE = (By.ID, "type")
    FROM_ACCOUNT = (By.ID, "fromAccountId")
    SUBMIT = (By.CSS_SELECTOR, "input[value='Open New Account']")
    RESULT = (By.ID, "openAccountResult")
    NEW_ACCOUNT_ID = (By.ID, "newAccountId")

    def open_account(self, account_type=SAVINGS, from_account_id=None):
        accounts = self.wait_for_options(self.FROM_ACCOUNT)
        self.select_by_value(self.TYPE, account_type)
        self.select_by_value(self.FROM_ACCOUNT, from_account_id or accounts[0])
        self.click(self.SUBMIT)
        self.find(self.RESULT)
        return self.text_of(self.NEW_ACCOUNT_ID)
