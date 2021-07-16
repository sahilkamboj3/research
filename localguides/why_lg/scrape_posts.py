import os
import pandas as pd
from os import path
import requests as re
from bs4 import BeautifulSoup
from datetime import datetime as dt

"""
Post info:
Author
URL
Author Level
Text
Likes
People tagged
People tagged URL
Date posted
"""

txt_file = 'posts.txt'
csv_file = 'posts.csv'


def convert_date_time(date, time):
    combined_date_time = date + ' ' + time
    time = dt.strptime(combined_date_time, '%m-%d-%Y %I:%M %p')
    res_date_time = time.strftime('%m-%d-%Y %I:%M %p')
    return res_date_time


def check_for_posts_txt(txt_file):
    cur_dir = path.dirname(__file__)

    if txt_file not in os.listdir(cur_dir):
        with open(txt_file, 'w') as f:
            pass

        return False

    return True


check_for_posts_txt(txt_file)
does_csv_exist = check_for_posts_txt(csv_file)

columns = [
    'author',
    'url',
    'author_level',
    'text',
    'likes',
    'people_tagged',
    'people_tagged_url',
    'date'
]

if not does_csv_exist:
    df = pd.DataFrame(columns=columns)
    df.to_csv('posts.csv', index=False)

for page_num in range(1, 6):
    print(page_num)

    post_data = []
    URL = f'https://www.localguidesconnect.com/t5/Help-Desk/Why-be-a-Local-Guide/ba-p/867121/page/{page_num}#comments'  # noqa
    res = re.get(URL, headers={})

    with open(txt_file, 'w') as f:
        f.write(res.text)

    with open(txt_file) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    div_tag = soup.find(
        'div', {'class', 'CommentList lia-component-comment-list'})
    post_tags = div_tag.find_all('div', {'class', 'lia-panel-message'})

    for post in post_tags:
        name_tag = post.find('a', {'class', 'lia-user-name-link'})

        if name_tag is None:
            author = 'Anonymous'
            url = 'Anonymous'
            level = 'Anonymous'
        else:
            author = name_tag.find('span').text
            url = name_tag['href']
            level = post.find(
                'div', {'class', 'lia-message-author-rank'}).text.rstrip().lstrip()

        date = post.find('span', {'class', 'local-date'}).text
        time = post.find('span', {'class', 'local-time'}).text

        res_date_time = convert_date_time(date.strip('\u200e'), time)
        likes = post.find(
            'span', {'class', 'MessageKudosCount'}).text.rstrip().lstrip()

        text_div = post.find('div', {'class', 'lia-message-body-content'})
        name_tagged_tag = text_div.find('a')

        if name_tagged_tag:
            tagged_url = name_tagged_tag['href'].lstrip().rstrip()
            if tagged_url[:3] == '/t5':
                name_tagged = name_tagged_tag.text
                name_tagged_url = 'https://www.localguidesconnect.com/' + \
                    name_tagged_tag['href'].lstrip().rstrip()
            else:
                name_tagged = 'None'
                name_tagged_url = 'None'
        else:
            name_tagged = 'None'
            name_tagged_url = 'None'

        post_text = ''
        for p_tag in text_div.find_all('p'):
            post_text += p_tag.text + ' '

        data = [author, url, level, post_text, int(likes),
                name_tagged, name_tagged_url, res_date_time]
        post_data.append(data)

        print('---------------------------------------------------------------')
        print('Text: ', post_text)
        print()
        print('Author: ', author)
        print()
        # print('URL: ', url)
        # print()
        print('Level: ', level)
        print()
        print('Likes: ', int(likes))
        print()
        # print('Name Tagged: ', name_tagged)
        # print()
        # print('Name Tagged URL: ', name_tagged_url)
        # print()
        print('Date: ', res_date_time)
        print()

        # break
    orig_df = pd.read_csv('posts.csv')
    df = pd.DataFrame(data=post_data, columns=columns)
    new_df = pd.concat([orig_df, df])
    new_df.to_csv('posts.csv', index=False)
