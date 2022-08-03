from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup as bs
from config import CHROME_LOCATION

# Variables for searching for notifications
link = "https://edu.21-school.ru"
calendar = link + "/calendar"

# Options for webdriver
op = webdriver.ChromeOptions()
op.binary_location = CHROME_LOCATION
op.add_argument("--headless")


# Function to authentificate into platform
def auth_into_platform(
    driver: webdriver.Chrome = None,
    username: str = "elenemar",
):
    if not driver:
        driver = webdriver.Chrome(executable_path="chromedriver", options=op)
    if driver.current_url != link:
        driver.get(link)  # link = "https://edu.21-school.ru"
        elem = driver.find_element(by=By.NAME, value="username")
        elem.send_keys(f"{username}@student.21-school.ru")
        elem = driver.find_element(by=By.NAME, value="password")
        elem.send_keys(password)
        elem.send_keys(Keys.ENTER)
        print(f'- Trying to authorizate user "{username}"...')
        sleep(10)
        if "auth.sberclass.ru" in driver.current_url:
            driver.close()
            print("- Authorization failed!")
            return None
        print("- Authorization success!")
        return driver


# Function to get list of planned participant peer reviews
def get_ppr_list(driver: webdriver.Chrome):
    driver.get(calendar)
    # Need to somehow check if page loaded fully and successfully
    print(f"Getting calendar page data...")
    sleep(10)
    source_code = driver.page_source
    driver.close()
    content = bs(source_code, "lxml")
    current_date = (
        content.find("div")
        .find_next("div")
        .find_next_sibling("div")
        .find_next_sibling("div")
        .find_next_sibling("div")
        .find_next_sibling("div")
        .find_next("div")
        .find_next("div")
        .find_next("div")
        .find_next_sibling("div")
    )
    count = 0
    while len(current_date.get_attribute_list("class")) != 2:
        current_date = current_date.find_next_sibling("div")
        count += 1
    current_date_column = (
        content.find("div")
        .find_next("div")
        .find_next_sibling("div")
        .find_next_sibling("div")
        .find_next_sibling("div")
        .find_next_sibling("div")
        .find_next("div")
        .find_next("div")
        .find_next_sibling("div")
        .find_all("div")[count]
    )
    if len(current_date_column) == 0:
        return None
    else:
        events_list = list(dict())
        for event in current_date_column.children:
            style_str = event.get("style").split(";")
            height = int(style_str[1][9:-2]) // 14
            events_list.append(
                {
                    "end_time": "garbage",
                    "start_time": event.find_next("div").text,
                    "event": event.find_next("div").find_next("div").text,
                }
            )
            start_time = events_list[-1]["start_time"].split(":")
            start_time = int(start_time[0]) * 60 + int(start_time[1])
            end_time = start_time + height * 15
            hour, min = end_time // 60, end_time % 60
            hour = str(hour)
            if len(hour) < 2:
                hour = "0" + hour
            min = str(min)
            if len(min) == 1:
                min += "0"
            end_time = hour + ":" + min
            events_list[-1]["end_time"] = end_time
        return events_list


def get_today_events(username: str, password: str):
    driver = auth_into_platform(username=username, password=password)
    if driver is None:
        return None
    events = get_ppr_list(driver)
    return events
