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


# Chrome driver install
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.linkedin.com/')
sleep(2)

my_username = os.getenv('LINKEDIN_USERNAME', 'emaildummy773@gmail.com')
my_password = os.getenv('LINKEDIN_PASSWORD', 'e_dummy123')

try:
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'session_key')))
    username.send_keys(my_username)

    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'session_password')))
    password.send_keys(my_password)

    log_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sign-in-form__submit-btn--full-width')))
    log_in_button.click()
except TimeoutException:
    print("Error: Timed out waiting for login page to load")
    driver.quit()
    exit()

sleep(3)


profile_urls = ['https://www.linkedin.com/in/andrewyng/recent-activity/shares']


sel = Selector(text=driver.page_source)

posts= {}

with open('results.json', 'w', encoding='utf-8') as f:
    for profile in profile_urls:
        driver.get(profile)

        print(f'Getting {profile}')
        
        for i in range(2):
            try:
                # Wait for the button to be clickable
                button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button--full') and contains(@class, 'artdeco-button--secondary') and contains(@class, 'scaffold-finite-scroll__load-button')]")))
                button.click()
            except TimeoutException:
                print("Timed out waiting for button to be clickable")
            sleep(10)

        sel = Selector(text=driver.page_source)
        div_element = sel.xpath("//div[contains(@class, 'ember-view') and contains(@class, 'occludable-update')]")
        
        for element in div_element:
            post = element.xpath(".//div[contains(@class, 'update-components-text') and contains(@class, 'feed-shared-update-v2__commentary')]//span[@class='break-words']//span[@dir='ltr']").extract_first()
            if not post:
                continue

            cleaned_text = re.sub('<[^<]+?>', '', post)
            date = element.xpath(".//span[contains(@class, 'update-components-actor__sub-description')]/div[contains(@class, 'update-components-text-view') and contains(@class, 'white-space-pre-wrap') and contains(@class, 'break-words')]/span[@class='visually-hidden']/span").extract_first()
            if not date:
                continue
            date = re.sub('<[^<]+?>', '', date).split(' ')[0]
            posts.setdefault(date, set())
            posts[date].add(cleaned_text)

    posts = {key: list(value) for key, value in posts.items()}
    json.dump(posts, f, ensure_ascii=False)

driver.quit()

