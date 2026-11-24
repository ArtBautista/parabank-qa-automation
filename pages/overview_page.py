"""Accounts Overview: the landing page after login."""
from decimal import Decimal
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
class OverviewPage(BasePage):
    path = "/overview.htm"
    ACCOUNT_LINKS = (By.CSS_SELECTOR, "#accountTable tbody tr td a")
    ROWS = (By.CSS_SELECTOR, "#accountTable tbody tr")

    def wait_until_loaded(self):
        self.wait.until(lambda driver: "Accounts Overview" in driver.title)
        self.find(self.ACCOUNT_LINKS)
        return self

    def account_ids(self):
        self.find(self.ACCOUNT_LINKS)
        return [link.text.strip() for link in self.find_all(self.ACCOUNT_LINKS)]

    def balances(self):
        """{account_id: Decimal balance} read from the table."""
        result = {}
        for row in self.find_all(self.ROWS):
            cells = row.find_elements(By.TAG_NAME, "td")
            links = row.find_elements(By.TAG_NAME, "a")
            if links and len(cells) >= 2:
                amount = cells[1].text.replace("$", "").replace(",", "").strip()
                result[links[0].text.strip()] = Decimal(amount)
        return result
