"""Fixtures: API client, browser per test, signed-in session, screenshots on failure."""
import base64
import os
import re
import uuid
from pathlib import Path

import pytest

from config import IS_LOCAL, PASSWORD, USERNAME
from framework.api_client import ParaBankApi

SCREENSHOTS = Path("reports/screenshots")


def pytest_addoption(parser):
    parser.addoption("--browser", default=os.environ.get("BROWSER", "chrome"),
                     choices=["chrome", "firefox", "edge"])
    parser.addoption("--headless", action="store_true", default=os.environ.get("HEADLESS") == "1")


# ---------------------------------------------------------------- API fixtures
@pytest.fixture(scope="session")
def api():
    client = ParaBankApi()
    if IS_LOCAL:
        client.initialize_db()  # known starting data; never on the public site
    return client


@pytest.fixture(scope="session")
def customer(api):
    """The signed-in customer's record from the REST API."""
    return api.login(USERNAME, PASSWORD)


@pytest.fixture
def two_accounts(api, customer):
    """(from_id, to_id) for transfer tests; opens a second account if needed."""
    accounts = api.accounts(customer["id"])
    if len(accounts) < 2:
        api.create_account(customer["id"], 1, accounts[0]["id"])
        accounts = api.accounts(customer["id"])
    return str(accounts[0]["id"]), str(accounts[1]["id"])


@pytest.fixture
def unique_username():
    return f"qa{uuid.uuid4().hex[:8]}"


# ---------------------------------------------------------------- UI fixtures
@pytest.fixture
def driver(request):
    from selenium import webdriver

    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if os.environ.get("CHROME_BINARY"):  # e.g. /usr/bin/chromium in Debian CI images
            options.binary_location = os.environ["CHROME_BINARY"]
        service = None
        if os.environ.get("CHROMEDRIVER_PATH"):
            from selenium.webdriver.chrome.service import Service
            service = Service(executable_path=os.environ["CHROMEDRIVER_PATH"])
        drv = webdriver.Chrome(options=options, service=service)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        drv = webdriver.Firefox(options=options)
    else:
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        drv = webdriver.Edge(options=options)
    drv.set_window_size(1366, 900)
    yield drv
    drv.quit()


@pytest.fixture
def overview(driver):
    """A browser signed in as PARABANK_USER, on Accounts Overview."""
    from pages import LoginPage

    return LoginPage(driver).open().login(USERNAME, PASSWORD)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed or "driver" not in item.funcargs:
        return
    png_b64 = item.funcargs["driver"].get_screenshot_as_base64()
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"[^\w.-]", "_", item.nodeid)
    (SCREENSHOTS / f"{name}.png").write_bytes(base64.b64decode(png_b64))
    html = item.config.pluginmanager.getplugin("html")
    if html is not None:
        report.extras = getattr(report, "extras", []) + [html.extras.image(png_b64)]
