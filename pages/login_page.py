"""Login form in the left panel of every logged-out page."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.overview_page import OverviewPage
class LoginPage(BasePage):
    path = "/index.htm"
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    SUBMIT = (By.CSS_SELECTOR, "input[value='Log In']")
    ERROR = (By.CSS_SELECTOR, "#rightPanel p.error")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    FORGOT_LINK = (By.LINK_TEXT, "Forgot login info?")

    def submit_credentials(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def login(self, username, password):
        """Happy path: sign in and return the loaded Accounts Overview."""
        self.submit_credentials(username, password)
        return OverviewPage(self.driver).wait_until_loaded()

    def error_message(self):
        return self.text_of(self.ERROR)
