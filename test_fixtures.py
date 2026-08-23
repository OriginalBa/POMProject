import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DESKTOP_SIGN_UP = (By.XPATH, "//header//a[contains(@href, '/signup') and contains(text(), 'Sign up')]")
MOBILE_MENU_TOGGLE = (By.XPATH, "//button[@aria-label='Toggle navigation' or contains(@class, 'hamburger')]")
MOBILE_SIGN_UP = (By.XPATH,
                  "//header//div[contains(@class, 'Actions')]//a[contains(@href, '/signup')] | //header//a[contains(text(), 'Sign up')]")


@allure.feature("Регистрация")
@allure.story("Отображение кнопки Sign Up на Desktop")
def test_desktop_sign_up_button(setup_browser):
    driver, device_type = setup_browser
    with allure.step("Проверка типа устройства"):
        if device_type == "mobile":
            pytest.skip("Пропускаем: это мобильное разрешение, десктопный тест не подходит")
    with allure.step("Ожидание появления кнопки"):
        sign_up_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(DESKTOP_SIGN_UP)
        )
    with allure.step("Проверка видимости кнопки"):
        assert sign_up_btn.is_displayed(), "Кнопка Sign up не отображается на десктопе"


@allure.feature("Регистрация")
@allure.story("Отображение кнопки Sign Up на Mobile")
def test_mobile_sign_up_button(setup_browser):
    driver, device_type = setup_browser
    with allure.step("Проверка типа устройства"):
        if device_type == "desktop":
            pytest.skip("Пропускаем: это десктопное разрешение, мобильный тест не подходит")
    with allure.step("Открываем мобильное меню"):
        menu_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(MOBILE_MENU_TOGGLE)
        )
    menu_button.click()
    with allure.step("Ожидание появления кнопки"):
        sign_up_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(MOBILE_SIGN_UP)
        )
    with allure.step("Проверка видимости кнопки"):
        assert sign_up_btn.is_displayed(), "Кнопка Sign up не отображается в мобильном меню"
