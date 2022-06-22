from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup as bs

# Variables for searching for notifications
link = "https://edu.21-school.ru"
calendar = link + "/calendar"

# Options for webdriver
op = webdriver.ChromeOptions()
op.add_argument("--headless")


# Function to authentificate into platform
def auth_into_platform(
    driver: webdriver.Chrome = None,
    username: str = "elenemar",
    password: str = "RepusSotnad1702",
):
    if not driver:
        driver = webdriver.Chrome(options=op)
    if driver.current_url != link:
        driver.get(link)
        elem = driver.find_element(by=By.NAME, value="username")
        elem.send_keys(f"{username}@student.21-school.ru")
        elem = driver.find_element(by=By.NAME, value="password")
        elem.send_keys(password)
        elem.send_keys(Keys.ENTER)
        print("STEP 1")
        sleep(5)
        if "auth.sberclass.ru" in driver.current_url:
            return None
        driver.get(calendar)
        sleep(5)
        print("STEP 2")
        source_code = driver.page_source
        driver.close()
        print("STEP 3")
        return source_code


# Function to get list of planned participant peer reviews
def get_ppr_list(source_code: str):
    soup = bs(source_code, "lxml")
    current_date = (
        soup.find("div")
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
        soup.find("div")
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
    source_code = auth_into_platform(username=username, password=password)
    if source_code is None:
        return None
    else:
        return get_ppr_list(source_code)
