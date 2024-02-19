from pathlib import Path

import pytest

from selenium import webdriver


@pytest.fixture
def browser():
    """
    Returns a Chrome browser, with the driver located at chromedriver-linux64/
    """
    path = Path(__file__).parent.parent / 'chromedriver-linux64' / 'chromedriver'
    service = webdriver.ChromeService(str(path))
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
