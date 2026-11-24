"""Request Loan: amount, down payment and the account that pays the down payment."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RequestLoanPage(BasePage):
    path = "/requestloan.htm"

    AMOUNT = (By.ID, "amount")
    DOWN_PAYMENT = (By.ID, "downPayment")
    FROM_ACCOUNT = (By.ID, "fromAccountId")
    SUBMIT = (By.CSS_SELECTOR, "input[value='Apply Now']")
    RESULT = (By.ID, "requestLoanResult")
    STATUS = (By.ID, "loanStatus")
    PROVIDER = (By.ID, "loanProviderName")
    APPROVED = (By.ID, "loanRequestApproved")
    DENIED = (By.ID, "loanRequestDenied")
    NEW_ACCOUNT_ID = (By.ID, "newAccountId")
    ERROR = (By.ID, "requestLoanError")

    def apply(self, amount, down_payment, from_account_id=None):
        accounts = self.wait_for_options(self.FROM_ACCOUNT)
        self.type(self.AMOUNT, amount)
        self.type(self.DOWN_PAYMENT, down_payment)
        self.select_by_value(self.FROM_ACCOUNT, from_account_id or accounts[0])
        self.click(self.SUBMIT)
        if self.wait_for_any_visible(self.RESULT, self.ERROR) == self.ERROR:
            raise AssertionError(f"ParaBank showed an error: {self.text_of(self.ERROR)}")
        self.wait.until(lambda d: self.find_all(self.STATUS)[0].text.strip() != "")
        return self.text_of(self.STATUS)

    def denial_message(self):
        return self.text_of((By.CSS_SELECTOR, "#loanRequestDenied .error"))
