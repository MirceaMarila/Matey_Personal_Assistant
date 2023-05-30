from core.web_driver import ChromeDriver, ElementFinder
from core.web_elements import Button, TextBox, GenericElement
import openai


def chat_gpt(search_text):
    openai.api_key = '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'
    model_engine = "text-davinci-003"
    prompt = search_text + " give me just the result"

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response



# print(chat_gpt("when did the ww1 started?"))

# //span[text()="Verify you are human"]/preceding-sibling::span
# driver = ChromeDriver(options=['--incognito'])
#     finder = ElementFinder(driver)

    # driver.get("https://chat.openai.com/")
    # driver.maximize_window()
    # Button(driver, finder, xpath="//div[text()=\"Log in\"]").click()
    # Button(driver, finder, xpath="//span[text()=\"Verify you are human\"]/preceding-sibling::span").click()