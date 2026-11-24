"""Shared Page Object behaviour: explicit waits, element helpers and the left menu."""
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from config import BASE_URL, TIMEOUT


class BasePage:
    path = "/index.htm"

    TITLE = (By.CSS_SELECTOR, "#rightPanel h1.title")
    WELCOME = (By.CSS_SELECTOR, "#leftPanel .smallText")
    LOG_OUT = (By.LINK_TEXT, "Log Out")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def open(self):
        self.driver.get(BASE_URL + self.path)
        return self

    # ------------------------------------------------------------ element helpers
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(str(text))

    def text_of(self, locator):
        return self.find(locator).text.strip()

    def select_by_value(self, locator, value):
        Select(self.find(locator)).select_by_value(str(value))

    def wait_for_options(self, select_locator, minimum=1):
        """Account dropdowns are filled by an AJAX call after the page loads.

        Waits until the <select> holds at least `minimum` options and returns their values.
        Works with any locator type (ID, NAME, CSS), because it finds the select first and
        then its <option> children.
        """
        def options_loaded(driver):
            try:
                select = driver.find_element(*select_locator)
                values = [o.get_attribute("value")
                          for o in select.find_elements(By.TAG_NAME, "option")]
            except (NoSuchElementException, StaleElementReferenceException):
                return False  # page still rendering, or the list is being rebuilt
            return values if len(values) >= minimum else False

        return self.wait.until(options_loaded)

    def is_visible(self, locator, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ------------------------------------------------------------ shared page parts
    @property
    def heading(self):
        """Text of the h1.title currently shown.

        ParaBank pages hold several h1.title elements (form, result, error) and show one at a
        time, so the first match in the DOM is often a hidden one.
        """
        return self.first_visible_text(self.TITLE)

    def first_visible_text(self, locator):
        def shown(driver):
            for element in driver.find_elements(*locator):
                if element.is_displayed() and element.text.strip():
                    return element.text.strip()
            return False

        return self.wait.until(shown)

    def wait_for_any_visible(self, *locators):
        """Return the first locator (of several) whose element becomes visible."""
        def any_shown(driver):
            for locator in locators:
                if any(e.is_displayed() for e in driver.find_elements(*locator)):
                    return locator
            return False

        return self.wait.until(any_shown)

    def welcome_text(self):
        return self.text_of(self.WELCOME)

    def go_to(self, menu_link_text):
        self.click((By.LINK_TEXT, menu_link_text))

    def log_out(self):
        self.click(self.LOG_OUT)
