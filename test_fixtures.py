import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DESKTOP_SIGN_UP = (By.XPATH, "//header//a[contains(@href, '/signup') and contains(text(), 'Sign up')]")
MOBILE_MENU_TOGGLE = (By.XPATH, "//button[@aria-label='Toggle navigation' or contains(@class, 'hamburger')]")
MOBILE_SIGN_UP = (By.XPATH,
                  "//header//div[contains(@class, 'Actions')]//a[contains(@href, '/signup')] | //header//a[contains(text(), 'Sign up')]")


def test_desktop_sign_up_button(setup_browser):
    driver, device_type = setup_browser
    if device_type == "mobile":
        pytest.skip("Пропускаем: это мобильное разрешение, десктопный тест не подходит")
    sign_up_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(DESKTOP_SIGN_UP)
    )
    assert sign_up_btn.is_displayed(), "Кнопка Sign up не отображается на десктопе"


def test_mobile_sign_up_button(setup_browser):
    driver, device_type = setup_browser
    if device_type == "desktop":
        pytest.skip("Пропускаем: это десктопное разрешение, мобильный тест не подходит")
    menu_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(MOBILE_MENU_TOGGLE)
    )
    menu_button.click()
    sign_up_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(MOBILE_SIGN_UP)
    )
    assert sign_up_btn.is_displayed(), "Кнопка Sign up не отображается в мобильном меню"
