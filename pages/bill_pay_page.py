"""Bill Pay: send money from one of the customer's accounts to a payee."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

def by_name(name):
    return (By.NAME, name)
class BillPayPage(BasePage):
    path = "/billpay.htm"
    FIELDS = {
        "name": "payee.name",
        "street": "payee.address.street",
        "city": "payee.address.city",
        "state": "payee.address.state",
        "zip_code": "payee.address.zipCode",
        "phone": "payee.phoneNumber",
        "account": "payee.accountNumber",
        "verify_account": "verifyAccount",
        "amount": "amount",
    }

    FROM_ACCOUNT = by_name("fromAccountId")
    SUBMIT = (By.CSS_SELECTOR, "input[value='Send Payment']")
    RESULT = (By.ID, "billpayResult")
    RESULT_PAYEE = (By.ID, "payeeName")
    RESULT_FROM = (By.ID, "fromAccountId")

    ERRORS = {
        "name": "validationModel-name",
        "account": "validationModel-account-empty",
        "verify_mismatch": "validationModel-verifyAccount-mismatch",
        "amount": "validationModel-amount-empty",
    }

    def fill(self, **values):
        self.wait_for_options(self.FROM_ACCOUNT)
        for key, value in values.items():
            self.type(by_name(self.FIELDS[key]), value)

    def pay(self, **values):
        self.fill(**values)
        self.click(self.SUBMIT)
        self.find(self.RESULT)
        return self

    def submit(self):
        self.click(self.SUBMIT)

    def error(self, key):
        return self.text_of((By.ID, self.ERRORS[key]))
