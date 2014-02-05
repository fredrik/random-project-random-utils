import time

# don't panic: http://selenium-python.readthedocs.org/en/latest/api.html


def displayed_after_wait(browser, css_selector, timeout=10):
    """
    Continually tests to see whether an element has become displayed before timing out
    """
    end = time.time() + timeout
    while time.time() < end:
        if browser.css(css_selector).is_displayed():
            return True
        time.sleep(0.5)
    return False
