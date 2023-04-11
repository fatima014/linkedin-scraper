import json
import re
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

my_username='emaildummy773@gmail.com'
my_password='e_dummy123'
username = driver.find_element(By.NAME, 'session_key')
username.send_keys(my_username) # username field

password = driver.find_element(By.NAME, 'session_password')
password.send_keys(my_password) # password field
sleep(7)

log_in_button = driver.find_element(By.CLASS_NAME,'sign-in-form__submit-btn--full-width') # submit button

log_in_button.click() # click the submit button
sleep(3)


profile_urls = ['https://www.linkedin.com/in/andrewyng/recent-activity/','https://www.linkedin.com/in/paulsavery/recent-activity/', 'https://www.linkedin.com/in/yann-lecun/recent-activity/', 'https://www.linkedin.com/in/michael-gschwind-3704222/recent-activity/', 'https://www.linkedin.com/in/tonyrobin/recent-activity/']


sel = Selector(text=driver.page_source)

posts= {}
count = 0

with open('results.json', 'w', encoding='utf-8') as f:
    for profile in profile_urls:
        driver.get(profile)

        print(f'Getting {profile}')
        
        try:
            # Wait for the button to be clickable
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button--full') and contains(@class, 'artdeco-button--secondary') and contains(@class, 'scaffold-finite-scroll__load-button')]")))
            button.click()
        except TimeoutException:
            print("Timed out waiting for button to be clickable")

        sleep(10)
        sel = Selector(text=driver.page_source)
        elements = sel.xpath("//div[contains(@class, 'ember-view') and contains(@class, 'occludable-update')]//div[contains(@class, 'update-components-text') and contains(@class, 'feed-shared-update-v2__commentary')]//span[@class='break-words']//span[@dir='ltr']")

        date = sel.xpath("//div[contains(@class, 'ember-view') and contains(@class, 'occludable-update')]//span[contains(@class, 'update-components-actor__sub-description')]/div[contains(@class, 'update-components-text-view') and contains(@class, 'white-space-pre-wrap') and contains(@class, 'break-words')]/span[@class='visually-hidden']/span")
        if profile == 'https://www.linkedin.com/in/andrewyng/recent-activity/':
            print(f'number of dates: {len(date)}')
            print(f'number of elements: {len(elements)}')
        for i, element in enumerate(elements):
            text = element.extract()
            cleaned_text = re.sub('<[^<]+?>', '', text)
            date[i] = re.sub('<[^<]+?>', '', date[i].extract())
            
            date[i] = date[i].split(' ')[0]
            if date[i] not in posts:
                posts.setdefault(date[i], [])
            posts[date[i]].append(cleaned_text)
    json.dump(posts, f, ensure_ascii=False)
        
# for date in posts:
#     print(f'date: {date}')
#     count += len(posts[date])
#     print(count)
# print(count)
