import os

import allure
import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import attach


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        help='Browser version for all tests',
        default='100.0',
        choices=['100.0', '99.0', '120.0', '121.0', '122.0']
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser.config.base_url = 'https://demoqa.com'
    browser.config.window_height = 1080
    browser.config.window_width = 1920
    options = Options()
    options.page_load_strategy = 'eager'
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    user_login = os.getenv('SELENOID_LOGIN')
    user_password = os.getenv('SELENOID_PASSWORD')
    selenoid_url = os.getenv('SELENOID_URL')
    driver = webdriver.Remote(command_executor=f'https://{user_login}:{user_password}@{selenoid_url}/wd/hub',
                              options=options)
    browser.config.driver = driver

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()
