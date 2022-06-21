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
        if "auth.sberclass.ru" in driver.current_url:
            return None
        sleep(5)
        driver.get(calendar)
        sleep(5)
        source_code = driver.page_source
        driver.close()
        return source_code


# Function to get list of planned participant peer reviews
def get_ppr_list(source_code: str):
    soup = bs(source_code, "lxml")
    button_orient = soup.find("button")
    for _ in range(2):
        button_orient = button_orient.find_next("button")
    print(button_orient)
    current_date = button_orient.find_previous("div")
    print(current_date)
    count = 0
    while len(current_date.get_attribute_list("class")) != 2:
        current_date = current_date.find_previous("div")
        count += 1
    calendars = soup.find(
        "div",
    )
    count = 7 - 1 - count
    current_date_column = calendars.find_next("div")
    for _ in range(count):
        current_date_column = current_date_column.find_next("div")
    print(current_date_column)
    if len(current_date_column) == 0:
        return None
    else:
        events_list = list(dict())
        for event in current_date_column.children:
            events_list.append(
                {
                    "time": event.find_next("div").text,
                    "event": event.find_next("div").find_next("div").text,
                }
            )
        return events_list


def get_today_events(username: str, password: str):
    source_code = auth_into_platform(username=username, password=password)
    events_list = get_ppr_list(source_code)
    return events_list
