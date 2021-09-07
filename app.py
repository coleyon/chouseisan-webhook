import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

WAIT_TIMEOUT = 10

if __name__ == "__main__":

    # make options
    selenium_url = os.getenv("SELENIUM_URL", default="http://localhost:4444/wd/hub")

    with webdriver.Remote(
        command_executor=selenium_url,
        desired_capabilities=DesiredCapabilities.CHROME,
    ) as driver:
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        driver.get("https://chouseisan.com")

        event_name_input = driver.find_element(By.XPATH, '//*[@id="name"]')
        memo_input = driver.find_element(By.XPATH, '//*[@id="comment"]')
        dates_input = driver.find_element(By.XPATH, '//*[@id="kouho"]')
        create_button = driver.find_element(By.XPATH, '//*[@id="createBtn"]')

        event_name_input.send_keys("testeasdasd")
        memo_input.send_keys("testeasdasd")
        dates_input.send_keys("testeasdasd")
        # create_button.click()
