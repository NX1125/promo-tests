import pytest

from test_promo.conftest import browser


@pytest.fixture
def admin_browser(browser):
    """
    Returns a browser at localhost:4200
    """
    browser.get('http://localhost:4200')
    return browser
