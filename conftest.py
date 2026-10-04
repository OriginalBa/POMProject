import pytest
from utils import attach
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

DESKTOP = [(1920, 1080), (1440, 900)]
MOBILE = [(375, 812), (414, 896)]
ALL_SIZES = DESKTOP + MOBILE

BREAKPOINT_WIDTH = 1012


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        choices=("chrome", "firefox", "edge"),
        help="Браузер для запуска тестов: chrome, firefox, edge"
    )
    parser.addoption(
        "--browser_version",
        default="100.0",
        help="Browser version to use"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )


def _make_driver(width, height, browser_name, browser_version, headless):
    if browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
    elif browser_name == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
    else:
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        if headless:
            options.add_argument("--headless=new")

    options.browser_version = browser_version
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": False,
        "version": browser_version
    })

    driver = webdriver.Remote(
        command_executor="https://user1:1234@selenoid.qa.guru/wd/hub",
        options=options
    )

    driver.set_window_size(width, height)
    return driver


@pytest.fixture(params=ALL_SIZES)
def setup_browser(request):
    width, height = request.param
    browser_name = request.config.getoption("--browser").lower()
    browser_version = request.config.getoption("--browser_version")
    headless = request.config.getoption("--headless")
    driver = _make_driver(width, height, browser_name, browser_version, headless)
    driver.get("https://github.com")
    device_type = "desktop" if width >= BREAKPOINT_WIDTH else "mobile"
    yield driver, device_type

    try:
        attach.add_screenshot(driver)
        attach.add_page_source(driver)
        if browser_name in ("chrome", "edge"):
            attach.add_console_logs(driver)
        attach.add_video(driver)
    finally:
        driver.quit()
