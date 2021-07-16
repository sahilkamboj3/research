import pandas as pd
import os
from os import path
import requests
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import langid

"""
COLUMNS:
1. username
2. date
3. forum_type (here General Discussion)
4. number of likes received
5. title
6. dummy if images are present
7. text (you need to click it to see in full — is it a problem? if it is, let’s at least collect visible text)
8. Note that some results additionally display a field called "Show results in replies (9)” — I would like that number if possible. 
9. Additionally, do you think it will be reasonable to collect posts in English only? I am contemplating on this, because even if the post is not in English, I can still have a COVID dummy for it and then use other text-irrelevant user characteristics for analysis. Perhaps we can think of some “filter” in the code that can be used when needed. 
"""

COLUMNS = [
    'id',
    'username',
    'user-url',
    'title',
    'likes',
    'post_type',
    'text',
    'replies',
    'date'
]


def check_files():
    BASE_DIR = path.dirname(__file__)
    files_dict = {'covid.txt': False, 'covid2.csv': False}

    for filename in files_dict.keys():
        if filename in os.listdir(BASE_DIR):
            files_dict[filename] = True

    if not files_dict['covid.txt']:
        with open('covid.txt', 'w') as f:
            f.write('')

    if not files_dict['covid2.csv']:

        df = pd.DataFrame(columns=COLUMNS, data={})
        df.to_csv('covid2.csv', index=False)


def gather_data(start=1, end=2):
    def convert_datetime_given_date_and_time(date, time):
        date = date.replace("&lrm;", "")
        date = date.replace("\u200e", "")
        datetime_str = f"{date} {time}"

        time_contents = datetime.strptime(datetime_str, "%m-%d-%Y %I:%M %p")

        return time_contents

    def convert_datetime_given_datetime(timestamp):
        # date = date.replace("&lrm;", "")
        # date = date.replace("\u200e", "")
        # datetime_str = f"{date} {time}"
        timestamp = timestamp.replace("&lrm;", "").replace("\u200e", "")

        time_contents = datetime.strptime(timestamp, "%m-%d-%Y %I:%M %p")

        return time_contents

    def replace_text(text, strings):
        for string in strings:
            text = text.replace(string, "")

        return text

    def sleep(start=5, end=10):
        num = random.randint(start, end)
        print(str(num) + 's')
        time.sleep(num)

    page_num = start
    query_size = 40
    headers = {
    }
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}  # noqa

    while page_num <= end:
        print(f"Page Num: {page_num}")
        data_rows = []

        BASE_URL = f"https://www.localguidesconnect.com/t5/forums/searchpage/tab/message?q=covid&advanced=true&page={page_num}&collapse_discussion=true&search_type=thread&search_page_size={query_size}"  # noqa
        res = requests.get(BASE_URL, headers=headers)

        with open('covid.txt', 'w') as f:
            f.write(res.text)

        with open('covid.txt', 'r') as f:
            text = f.read()

        soup = BeautifulSoup(text, 'html.parser')
        posts = soup.find_all("div", {"class", "lia-message-view-wrapper"})

        # print("Posts", posts)

        for post in posts:
            strings_to_replace = ["\n", "\t", "\xa0", "\u2003"]
            text = post.find(
                "div", {"class", "lia-truncated-body-container"}).text
            text = replace_text(text, strings_to_replace)

            if not langid.classify(text)[0] == 'en':
                continue

            title = post.find("a", {"class", "page-link"}).text

            username_a_tag = post.find(
                "a", {"class", "lia-user-name-link"})
            if username_a_tag:
                username = username_a_tag.find("span").text
                user_url = username_a_tag['href']
                final_slash_idx = username_a_tag['href'].rfind('/')
                user_id = username_a_tag['href'][final_slash_idx+1:]
            else:
                username = user_url = user_id = "Anonymous"

            post_type = post.find(
                "a", {"class", "lia-component-common-widget-link"}).text

            likes_tag = post.find_all("a", {"class", "lia-kudos-count-link"})
            if likes_tag:
                likes_str = likes_tag[0].text.replace(',', '')
                space_idx = likes_str.find(' ')
                likes = int(likes_str[0:space_idx])
            else:
                likes = 0

            # strings_to_replace = ["\n", "\t", "\xa0", "\u2003"]
            # text = post.find(
            #     "div", {"class", "lia-truncated-body-container"}).text
            # text = replace_text(text, strings_to_replace)

            reply = post.find("a", {"class", "lia-replies-toggle-link"})
            if reply:
                opening_bracket_idx = reply.text.rfind("(")
                closing_bracket_idx = reply.text.rfind(")")
                reply_count = int(
                    reply.text[opening_bracket_idx+1:closing_bracket_idx])
            else:
                reply_count = 0

            try:
                time_tags = post.find_all("span", {"class", "local-time"})
                date_tags = post.find_all("span", {"class", "local-date"})
                post_datetime = convert_datetime_given_date_and_time(
                    date_tags[0].text, time_tags[0].text)
            except IndexError:
                datetime_tag = post.find_all(
                    "span", {"class", "local-friendly-date"})
                post_datetime = convert_datetime_given_datetime(
                    datetime_tag[0]['title'])

            data_rows.append([
                user_id,
                username,
                user_url,
                title.strip(),
                likes,
                post_type,
                # text if len(text) > 2 and lang.detect_language(
                # ) == "en" else "None",
                text if len(text) > 0 else "None",
                reply_count,
                post_datetime
            ])

        # print("Data rows:\n", data_rows)

        orig_df = pd.read_csv('covid2.csv')
        new_data_df = pd.DataFrame(columns=COLUMNS, data=data_rows)
        new_df = pd.concat([orig_df, new_data_df])
        new_df.to_csv('covid2.csv', index=False)

        if page_num % 10 == 0 and page_num != end:
            sleep(start=120, end=180)
        else:
            sleep()

        page_num += 1


check_files()
# gather_data(start=100, end=100)
# gather_data(start=51, end=51)
# COUNT - 900 (up until page 90) except pages 64

gather_data(start=31, end=79)  # goes to page 79
