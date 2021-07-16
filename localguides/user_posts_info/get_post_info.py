from urllib3.exceptions import ReadTimeoutError
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests as re
from datetime import datetime as dt

LG_TRENDING = 'https://www.localguidesconnect.com/t5/custom/page/page-id/Custom-Trending-Page'
BASE_USER_URL = 'https://www.localguidesconnect.com/t5/user/viewprofilepage/user-id/'
BASE_LG_URL = 'https://www.localguidesconnect.com'
HEADERS = ['id', 'title', 'likes', 'comments', 'content',
           'cleaned_date', 'post_url', 'user_url']
TIMEOUT_LENGTH = 10
SLEEP_TIME = 1


def get_user_ids_from_csv(relative_path):
    df = pd.read_csv(relative_path)
    return df['id']


def sleep(sleep_time):
    # time.sleep(sleep_time)
    return


def get_posts_for_ids(user_ids, csv_filename, data_dir_rel_path="data/user_posts_info/"):
    def clean_user_url(user_id):
        return BASE_USER_URL + str(user_id)

    def append_to_data_csv_file(posts):
        orig_df = pd.read_csv(data_dir_rel_path + csv_filename)
        append_df = pd.DataFrame(columns=HEADERS, data=posts)
        new_df = pd.concat([orig_df, append_df])
        new_df.to_csv(data_dir_rel_path + csv_filename, index=False)

    if not os.path.exists(data_dir_rel_path):
        print(f'Created {csv_filename} in {data_dir_rel_path}')
        os.mkdir(data_dir_rel_path)
        df = pd.DataFrame(columns=HEADERS)
        df.to_csv(data_dir_rel_path + csv_filename, index=False)

    if csv_filename not in os.listdir(data_dir_rel_path):
        print(f'Created {csv_filename}')
        df = pd.DataFrame(columns=HEADERS)
        df.to_csv(data_dir_rel_path + csv_filename, index=False)

    total_post_count = 0
    res_filename = 'user.txt'
    res_error_filename = 'id_errors.txt'
    posts_arr = []
    count = 1

    for user_id in user_ids:
        sleep(SLEEP_TIME)
        print(f'Retrieving user {user_id}, count is {count}')
        url = BASE_USER_URL + str(user_id)
        try:
            res = re.get(url, timeout=TIMEOUT_LENGTH)
        except (ReadTimeoutError, re.exceptions.Timeout, re.exceptions.ReadTimeout, re.exceptions.ConnectionError, TimeoutError):
            with open(res_error_filename, 'a') as f:
                content = f"{user_id}\n"
                f.write(content)
            continue

        with open(res_filename, 'w') as f:
            f.write(res.text)

        res_posts_arr = read_res_file(res_filename)
        total_post_count += len(res_posts_arr)

        for res_post in res_posts_arr:
            post = res_post
            post.insert(0, user_id)
            post.append(clean_user_url(user_id))

            posts_arr.append(post)

        if count % 5 == 0:
            append_to_data_csv_file(posts_arr)
            posts_arr = []

        print()
        count += 1

    print('------SUMMARY---------')
    print(f'Total posts: {total_post_count}')


def read_res_file(res_filename):
    def clean_date(timestamp):
        datetime_stamp = dt.strptime(timestamp, "%b %d, %Y")
        return dt.strftime(datetime_stamp, "%b %d, %Y")

    def clean_post_url(url):
        return BASE_LG_URL + url

    with open(res_filename, 'r') as f:
        text = f.read()

    soup = BeautifulSoup(text, "html.parser")
    posts_div = soup.find('div', {'id': 'posts'})

    if not posts_div:
        print('No posts')
        return []

    posts = posts_div.find_all('div', {'class': 'message-card'})

    if not posts or len(posts) == 0:
        print('No posts')
        return []

    len_posts = len(posts)

    res_posts_arr = []

    for post in posts:
        title_h4 = post.find('h4', {'class': 'message-content-subject'})
        title = post_url = None
        if title_h4:
            title = title_h4.find('a').text
            post_url = clean_post_url(title_h4.find('a')['href'])

        date_div = post.find('div', {'class': 'message-time-wrap'})
        date = cleaned_date = None
        if date_div:
            spans = date_div.find_all('span')
            if len(spans) == 1:
                date = spans[0].text.strip()
            else:
                date = spans[1].text.strip()

            cleaned_date = clean_date(date)

        likes_span = post.find('span', {'class': 'MessageKudosCount'})
        comments_a = post.find('a', {'class': 'comment-count'})
        likes = int(likes_span.text)
        comments = content = None

        if comments_a:
            comments = int(comments_a.text)
            _, content = get_comment_count_from_post_url(post_url)
        else:
            comments, content = get_comment_count_from_post_url(post_url)

        res_posts_arr.append(
            [title, likes, comments, content, cleaned_date, post_url])

    len_actual_posts = len(res_posts_arr)

    print(f'{len_posts} posts, {len_actual_posts} added')

    return res_posts_arr


def get_comment_count_from_post_url(url):
    def clean_post_content(content):
        content = content.replace('&nbsp;', '')
        return content

    post_filename = 'post.txt'
    try:
        res = re.get(url, timeout=TIMEOUT_LENGTH)
    except (ReadTimeoutError, re.exceptions.Timeout, re.exceptions.ReadTimeout, re.exceptions.ConnectionError, TimeoutError):
        print('Post page error')
        return None, None

    with open(post_filename, 'w') as f:
        f.write(res.text)
    with open(post_filename, 'r') as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')
    potential_comment_tags = soup.find_all('div', {'class': 'lia-text'})

    comments = None
    for comment_tag in potential_comment_tags:
        INVALID_STR = 'You must be a registered user to add a comment.'
        if 'comment' in comment_tag.text and INVALID_STR not in comment_tag.text:
            comment_text = comment_tag.text.strip()
            comment_text_cleaned = comment_text[0: comment_text.find(' ')]
            comments = int(comment_text_cleaned)

    post_content_div = soup.find('div', {'class': 'lia-message-body'})
    post_content = post_content_div .find(
        'div', {'class': 'lia-message-body-content'}).text
    post_content_cleaned = clean_post_content(post_content)

    return comments, post_content_cleaned


covid_rel_path = '../../data/covid/users.csv'
control_rel_path = '../../data/control/users.csv'
data_dir_rel_path = '../../data/user_posts_info/'

covid_ids = get_user_ids_from_csv(covid_rel_path)
control_ids = get_user_ids_from_csv(control_rel_path)

control_ids = control_ids.head(50)
print(len(control_ids))

#get_posts_for_ids(covid_ids, 'covid_user_posts_second.csv', data_dir_rel_path)
get_posts_for_ids(
    control_ids, 'control_user_posts_second.csv', data_dir_rel_path)
