import sys
import json
import re
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from parsel import Selector
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException


def is_later(interval1, interval2):
    """
    Check if interval2 occurs later in time than interval1.

    Args:
    - interval1 (str): First time interval (in the format "{number}{unit}")
    - interval2 (str): Second time interval (in the format "{number}{unit}")

    Returns:
    - bool: True if interval2 occurs later in time than interval1, False otherwise.
    """
    units = {"s": 1/(24*60*60),"m": 1/(24*60),"h": 1/24,"d": 1, "w": 7, "mo": 30, "yr": 365}  # Map of time units to days
    unit1 = re.sub(r"\d+", "", interval1)
    num1 = int(re.findall(r"\d", interval1)[0])
    unit2 = re.sub(r"\d+", "", interval2)
    num2 = int(re.findall(r"\d", interval2)[0])
    days1, days2 = num1 * units[unit1], num2 * units[unit2]  # Convert intervals to days
    return days2 > days1


if len(sys.argv) != 2:
    print("Usage: python script.py <week>")
    sys.exit(1)

try:
    week = int(sys.argv[1])
except ValueError:
    print("Error: week must be an integer")
    sys.exit(1)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.linkedin.com/')
sleep(2)

my_username = os.getenv('LINKEDIN_USERNAME', 'emaildummy773@gmail.com')
my_password = os.getenv('LINKEDIN_PASSWORD', 'e_dummy123')

try:
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'session_key')))
    username.send_keys(my_username)

    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'session_password')))
    password.send_keys(my_password)

    log_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, 'sign-in-form__submit-btn--full-width')))
    log_in_button.click()
except TimeoutException:
    print("Error: Timed out waiting for login page to load")
    driver.quit()
    exit()
except NoSuchElementException:
    print("Error: Cannot find login form elements")
    driver.quit()
    sys.exit(1)

sleep(3)


with open('profiles.json', 'r') as f:
    profile_urls = json.load(f)

profile_urls = [url.strip('/') + '/recent-activity/shares' for url in profile_urls]

pattern = r'https://(?!www\.)([a-z]+\.)?linkedin\.com'
profile_urls = [re.sub(pattern, 'https://www.linkedin.com', url)
                for url in profile_urls]

posts = {}


for profile in profile_urls:
    driver.get(profile)

    print(f'Getting {profile}')

    for i in range(2):
        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'artdeco-button--full') and contains(@class, 'artdeco-button--secondary') and contains(@class, 'scaffold-finite-scroll__load-button')]")))
            button.click()
        except TimeoutException:
            print("Timed out waiting for button to be clickable")
            continue

    try:
        sel = Selector(text=driver.page_source)
        div_element = sel.xpath(
            "//div[contains(@class, 'ember-view') and contains(@class, 'occludable-update')]")
    except StaleElementReferenceException:
        print("Stale element reference exception occurred")
        continue

    for element in div_element:
        post = element.xpath(
            ".//div[contains(@class, 'update-components-text') and contains(@class, 'feed-shared-update-v2__commentary')]//span[@class='break-words']//span[@dir='ltr']").extract_first()

        if not post:
            continue

        cleaned_text = re.sub('<[^<]+?>', '', post)
        date = element.xpath(
            ".//span[contains(@class, 'update-components-actor__sub-description')]/div[contains(@class, 'update-components-text-view') and contains(@class, 'white-space-pre-wrap') and contains(@class, 'break-words')]/span[@class='visually-hidden']/span").extract_first()

        if not date:
            continue

        date = re.sub('<[^<]+?>', '', date).split(' ')[0]
        if is_later(f'{week}mo', date):
            break
        posts.setdefault(date, [])
        posts[date].append(cleaned_text)
    with open('results.json', 'w', encoding='utf-8') as f:
        posts = {key: list(set(value)) for key, value in posts.items()}
        json.dump(posts, f, ensure_ascii=False)
    

driver.quit()
