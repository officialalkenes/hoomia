import pytest
from selenium.webdriver.common.keys import Keys

# @pytest.mark.selenium
def test_hello():
    text = "Hello World"
    assert text == "Hello World"

# @pytest.mark.selenium
# def test_admin_dashboard():