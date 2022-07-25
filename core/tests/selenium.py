import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope='module')
def chome_browser_setup(request):
    options = Options()
    options.headless = False
    browser = webdriver.chrome(options=options)
    yield browser
    browser.close()
