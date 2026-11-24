"""Transfer Funds between two of the customer's accounts."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class TransferPage(BasePage):
    path = "/transfer.htm"

    AMOUNT = (By.ID, "amount")
    FROM_ACCOUNT = (By.ID, "fromAccountId")
    TO_ACCOUNT = (By.ID, "toAccountId")
    SUBMIT = (By.CSS_SELECTOR, "input[value='Transfer']")
    RESULT = (By.ID, "showResult")
    RESULT_FROM = (By.ID, "fromAccountIdResult")
    RESULT_TO = (By.ID, "toAccountIdResult")
    AMOUNT_ERRORS = (By.CSS_SELECTOR, "[id='amount.errors']")
    ERROR = (By.ID, "showError")

    def account_options(self):
        return self.wait_for_options(self.FROM_ACCOUNT, minimum=2)

    def fill(self, amount, from_account_id, to_account_id):
        self.account_options()
        self.type(self.AMOUNT, amount)
        self.select_by_value(self.FROM_ACCOUNT, from_account_id)
        self.select_by_value(self.TO_ACCOUNT, to_account_id)

    def transfer(self, amount, from_account_id, to_account_id):
        self.fill(amount, from_account_id, to_account_id)
        self.click(self.SUBMIT)
        if self.wait_for_any_visible(self.RESULT, self.ERROR) == self.ERROR:
            raise AssertionError(f"ParaBank showed an error: {self.text_of(self.ERROR)}")
        return self

    def visible_amount_error(self):
        """Return the amount validation message being shown.

        If ParaBank shows a result or an error page instead, fail with what it showed, so the
        report says exactly how the page behaved.
        """
        shown = self.wait_for_any_visible(self.AMOUNT_ERRORS, self.RESULT, self.ERROR)
        if shown == self.RESULT:
            raise AssertionError("Invalid amount was accepted: 'Transfer Complete!' was shown")
        if shown == self.ERROR:
            raise AssertionError(f"ParaBank showed an error page: {self.text_of(self.ERROR)}")
        return next(e.text.strip() for e in self.find_all(self.AMOUNT_ERRORS) if e.is_displayed())
