"""Register page: customer details plus username and password."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
def field(name):
    return (By.ID, name)

def field_error(name):
    return (By.ID, f"{name}.errors")

class RegisterPage(BasePage):
    path = "/register.htm"

    FIELDS = {
    "first_name": "customer.firstName",
    "last_name": "customer.lastName",
    "street": "customer.address.street",
    "city": "customer.address.city",
    "state": "customer.address.state",
    "zip_code": "customer.address.zipCode",
    "phone": "customer.phoneNumber",
    "ssn": "customer.ssn",
    "username": "customer.username",
    "password": "customer.password",
    "confirm": "repeatedPassword",
    }

    SUBMIT = (By.CSS_SELECTOR, "input[value='Register']")
    SUCCESS_TEXT = (By.CSS_SELECTOR, "#rightPanel p")

    def fill(self, **values):
        for key, value in values.items():
            self.type(field(self.FIELDS[key]), value)

    def register(self, **values):
        self.fill(**values)
        self.click(self.SUBMIT)

    def error_for(self, key):
        return self.text_of(field_error(self.FIELDS[key]))
