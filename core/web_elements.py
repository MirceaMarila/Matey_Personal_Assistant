from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class WebElement:

    def __init__(self, driver, finder, xpath, clickable=True):
        self.driver = driver
        if clickable:
            finder.clickable_element(['xpath', xpath])
        else:
            finder.presence_of_element(['xpath', xpath])
        self.element = self.driver.find_element('xpath', xpath)

    def is_displayed(self):
        self.scroll_into_view()
        return self.element.is_displayed()

    def scroll_into_view(self):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", self.element)

        except:
            pass

    def is_displayed(self):
        self.scroll_into_view()
        return self.element.is_displayed()

    def get_text(self):
        self.scroll_into_view()
        return self.element.text or self.element.get_attribute("value")

    def click(self, double=False):
        self.scroll_into_view()
        try:
            if double:
                ActionChains(self.driver).double_click(self.element).perform()
            else:
                self.element.click()

        except:
            self.click_js()

    def click_js(self):
        self.scroll_into_view()
        self.driver.execute_script(f"arguments[0].click();", self.element)


class Button(WebElement):
    def __init__(self, driver, finder, xpath=None, clickable=True):
        super().__init__(driver, finder, xpath, clickable)


class TextBox(WebElement):
    def __init__(self, driver, finder, xpath=None, tag="input", tag2="textarea", text=None, attribute="placeholder",
                 attribute2="aria-label", attribute3="name", value=None):
        if not xpath:
            xpath = f"//{tag}[@{attribute}=\"{value if value else text}\"]|" \
                    f"//{tag}[@{attribute2}=\"{value if value else text}\"]|" \
                    f"//label[text()=\"{value if value else text}\"]/..//input[@type=\"number\"]|" \
                    f"//{tag}[@{attribute3}=\"{value.lower() if value else text.lower()}\"]|" \
                    f"//{tag2}[@{attribute3}=\"{value.lower() if value else text.lower()}\"]|" \
                    f"//{tag2}[@{attribute}=\"{value if value else text}\"]|" \
                    f"//{tag2}[@id=\"{value}\"]"

        super().__init__(driver, finder, xpath)

    def write_text(self, text):
        self.scroll_into_view()
        self.clear()
        self.element.send_keys(text)

    def append_text(self, text):
        self.scroll_into_view()
        self.element.send_keys(text)

    def clear(self):
        try:
            self.element.clear()
        except:
            pass
        self.element.send_keys(Keys.CONTROL, 'a', Keys.DELETE)

    def write_text_js(self, text):
        self.scroll_into_view()
        self.driver.execute_script(f"arguments[0].value = '{text}'", self.element)


class GenericElement(WebElement):
    def __init__(self, driver, finder, xpath=None, text=None, clickable=True):
        if not xpath:
            xpath = f"(//*[not(name()='script')][not(name()='style')][contains(text(), \"{text}\")]|" \
                    f"//*[not(name()='script')][not(name()='style')][@placeholder=\"{text}\"]|" \
                    f"//*[not(name()='script')][not(name()='style')][@value=\"{text}\"])[last()]"

        super().__init__(driver, finder, xpath, clickable)
