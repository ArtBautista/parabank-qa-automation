"""Find Transactions by id, date, date range or amount."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage



class FindTransactionsPage(BasePage):
    path = "/findtrans.htm"
    ACCOUNT = (By.ID, "accountId")
    AMOUNT = (By.ID, "amount")
    FIND_BY_AMOUNT = (By.ID, "findByAmount")
    TRANSACTION_ID = (By.ID, "transactionId")
    FIND_BY_ID = (By.ID, "findById")
    RESULTS = (By.CSS_SELECTOR, "#transactionTable tbody tr")
    RESULT_CONTAINER = (By.ID, "resultContainer")
    AMOUNT_ERROR = (By.ID, "amountError")
    TRANSACTION_ID_ERROR = (By.ID, "transactionIdError")

    def find_by_amount(self, account_id, amount):
        self.wait_for_options(self.ACCOUNT)
        self.select_by_value(self.ACCOUNT, account_id)
        self.type(self.AMOUNT, amount)
        self.click(self.FIND_BY_AMOUNT)
        self.find(self.RESULT_CONTAINER)
        return self

    def result_count(self):
        return len(self.find_all(self.RESULTS))

    def submit_transaction_id(self, account_id, transaction_id):
        self.wait_for_options(self.ACCOUNT)
        self.select_by_value(self.ACCOUNT, account_id)
        self.type(self.TRANSACTION_ID, transaction_id)
        self.click(self.FIND_BY_ID)
