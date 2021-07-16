import requests as re
import pandas as pd
from bs4 import BeautifulSoup
import time
from urllib3.exceptions import ReadTimeoutError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException
)


TIMEOUT_LENGTH = 10
LG_TRENDING_URL = 'https://www.localguidesconnect.com/t5/custom/page/page-id/Custom-Trending-Page'
PATH = "./chromedriver"
FILENAME = 'user_ids.csv'


def get_trending_user_ids():
    print('Getting trending user_ids...')

    xPath = '//a[text()="See more"]'
    post_titles_xpath = '//div[@class="message-card"]//div[@class="user-info"]//a'

    driver = webdriver.Chrome(PATH)
    driver.get(LG_TRENDING_URL)

    click_count = 1
    max_clicks = 100
    element_to_be_clickable_max_time_limit = 10

    while click_count <= max_clicks:
        # click see more logic
        try:
            element = WebDriverWait(driver, element_to_be_clickable_max_time_limit).until(
                EC.element_to_be_clickable((By.XPATH, xPath)))
        except TimeoutException:
            break

        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        try:
            element.click()
        except ElementNotInteractableException:
            break
        time.sleep(2)

        click_count += 1

    elements = driver.find_elements_by_xpath(post_titles_xpath)
    # user_ids = []
    count = 0

    for element in elements:
        try:
            url = element.get_attribute('href')
            res = re.get(url, timeout=TIMEOUT_LENGTH)

            soup = BeautifulSoup(res.text, 'html.parser')
            a_text = soup.find('a', {'class', 'lia-user-name-link'})['href']
            a_text_slash = a_text.rfind('/')

            user_id = a_text[a_text_slash+1:]

            orig_df = pd.read_csv(FILENAME)
            append_df = pd.DataFrame(columns=['id'], data=[user_id])
            new_df = pd.concat([orig_df, append_df])
            new_df.drop_duplicates(inplace=True)
            new_df.to_csv(FILENAME, index=False)

            count += 1
            # user_ids.append(user_id)
            print(f'{a_text} - {user_id}')
        except (StaleElementReferenceException, ReadTimeoutError, re.exceptions.Timeout, re.exceptions.ReadTimeout, re.exceptions.ConnectionError, TimeoutError):
            print(f'Seen exception - {count} - {user_id}')
            continue
        # except:
            # print(f'Weird exception - {count} - {user_id}')
            # continue

    driver.close()


#filename = 'user_ids.csv'
df = pd.DataFrame(columns=['id'])
# df.drop_duplicates(inplace=True)
df.to_csv(FILENAME, index=False)

#print(filename + ' created')


get_trending_user_ids()
