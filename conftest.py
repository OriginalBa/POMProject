import pytest
from selenium import webdriver

DESKTOP = [(1920, 1080), (1440, 900)]
MOBILE = [(375, 812), (414, 896)]
ALL_SIZES = DESKTOP + MOBILE

BREAKPOINT_WIDTH = 1012


def _make_driver(width, height):
    driver = webdriver.Chrome()
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
