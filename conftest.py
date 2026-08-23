import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DESKTOP = [(1920, 1080), (1440, 900)]
MOBILE = [(375, 812), (414, 896)]
ALL_SIZES = DESKTOP + MOBILE

BREAKPOINT_WIDTH = 1012


def _make_driver(width, height):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Remote(
        command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options, )
    # driver = webdriver.Chrome(options=options)
    driver.set_window_size(width, height)
    driver.get("https://github.com/")
    return driver


@pytest.fixture(params=ALL_SIZES)
def setup_browser(request):
    width, height = request.param
    driver = _make_driver(width, height)
    device_type = "desktop" if width >= BREAKPOINT_WIDTH else "mobile"
    yield driver, device_type
    driver.quit()
