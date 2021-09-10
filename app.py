import os
import requests
import json
import pytz
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import croniter


WAIT_TIMEOUT = 10
TODAY = dt.now(pytz.timezone(os.getenv("APP_TZ", default="Asia/Tokyo")))
BASE_URL = "https://chouseisan.com"
TITLE = "コンテンツ列車 {tgt_date}"
MEMOS = [
    "出欠は前日の21時頃までにはお願いしますm(_ _)m",
    "このリンクから参加表明ができます!",
    "ユーザ登録やログインは必要ないのでお気軽にどうぞ!",
]
CHOICES = ["早発便21:00～21:30発", "後発便22:00～22:30", "どちらでも可"]
DISCO_WEBHOOK_CONTENT = {
    "username": os.getenv("WEBHOOK_USER"),
    "content": TITLE,
    "embeds": [
        {
            "title": "",
            "url": "",
            "description": "\n".join(MEMOS),
            "color": 4312120,
            "fields": [
                {"name": "early", "value": CHOICES[0], "inline": True},
                {"name": "latest", "value": CHOICES[1], "inline": True},
                {"name": "any", "value": CHOICES[2], "inline": True},
            ],
        }
    ],
}


def get_next() -> dt:
    # TODO implement it
    return croniter(os.getenv("CRON"), TODAY).get_next(dt)


def is_notify_requiried() -> bool:
    # TODO implement it
    return True


def input_plan(url: str, driver: webdriver.Remote) -> str:
    # page load
    driver.get(url)
    # input and submit form
    current_url = driver.current_url
    event_name_input = driver.find_element(By.XPATH, '//*[@id="name"]')
    memo_input = driver.find_element(By.XPATH, '//*[@id="comment"]')
    dates_input = driver.find_element(By.XPATH, '//*[@id="kouho"]')
    create_button = driver.find_element(By.XPATH, '//*[@id="createBtn"]')
    event_name_input.send_keys(TITLE)
    memo_input.send_keys(MEMOS[0])
    dates_input.send_keys("\n".join(CHOICES))
    create_button.submit()
    # get event url
    WebDriverWait(driver, WAIT_TIMEOUT).until(EC.url_changes(current_url))
    list_url = driver.find_element(By.XPATH, '//*[@id="listUrl"]')
    return list_url.get_attribute("value")


if __name__ == "__main__":
    result = ""
    # web scraping
    selenium_url = os.getenv("SELENIUM_URL", default="http://localhost:4444/wd/hub")
    with webdriver.Remote(
        command_executor=selenium_url,
        desired_capabilities=DesiredCapabilities.CHROME,
    ) as driver:
        wait = WebDriverWait(driver, WAIT_TIMEOUT)
        driver.set_page_load_timeout(WAIT_TIMEOUT)
        driver.set_script_timeout(WAIT_TIMEOUT)
        driver.implicitly_wait(WAIT_TIMEOUT)
        result = input_plan(BASE_URL, driver)

    # web hooking
    content = DISCO_WEBHOOK_CONTENT.copy()
    content["embeds"][0]["title"] = result
    content["embeds"][0]["url"] = result
    response = requests.post(
        url=os.getenv("WEBHOOK_URL"),
        data=json.dumps(content),
        headers={"Content-Type": "application/json"},
        timeout=WAIT_TIMEOUT,
    )
