from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class ChromeDriver(webdriver.Chrome):
    def __init__(self, options=None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

        if options:
            for option in options:
                chrome_options.add_argument(option)

        super().__init__(executable_path=r"chromedriver.exe", options=chrome_options)


class ElementFinder:
    def __init__(self, driver):
        self.driver = driver
        self.web_driver_wait = WebDriverWait(driver, 10)

    def clickable_element(self, locator):
        return self.web_driver_wait.until(ec.element_to_be_clickable(locator))

    def visible_element(self, locator):
        return self.web_driver_wait.until(ec.visibility_of_element_located(locator))

    def presence_of_element(self, locator):
        return self.web_driver_wait.until(ec.presence_of_element_located(locator))

    def invisibility_of_element_located(self, locator):
        return self.web_driver_wait.until(ec.invisibility_of_element_located(locator))
