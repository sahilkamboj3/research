import pandas as pd
import random
from urllib3.exceptions import HTTPError
import os
from os import path
from scrape_class_lg_user import Scraper
from Util import UtilClass

# handle for 8639, 1327, 1328, 14142, 14881, 11891 separately

util = UtilClass()

"""
Sample URL: https://www.localguidesconnect.com/t5/user/viewprofilepage/user-id/14103  # noqa
"""

users_columns = [
    'id',
    'name',
    'level',
    'total_messages_posted',
    'total_likes_received',
    'total_likes_given',
    'description',  # None means no description
    'total_badges',
    'badges'  # array
]

likes_given_to_posts_columns = [
    'id',
    'name',
    'author',
    'author_url',
    'author_id',
    'post_title',
    'post_type',
    'total_replies',
    'total_likes',
    'icon',
    'date_posted'
]

likes_received_for_posts_columns = [
    'id',
    'name',
    'post_title',
    'post_type',
    'total_replies',
    'total_likes',
    'icon',
    'date_posted',
]

likes_received_from_users_columns = [
    'to_id',
    'to_name',
    'from_username',
    'from_id',
    'from_url',
    'from_level',
    'from_likes',
]

likes_given_to_users_columns = [
    'from_id',
    'from_name',
    'to_username',
    'to_id',
    'to_url',
    'to_level',
    'to_likes',
]


class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def create_csv_file(name):
    import pandas as pd
    from os import path

    columns_dic = {
        "users.csv": users_columns,
        "likes_given_to_posts.csv": likes_given_to_posts_columns,
        "likes_received_for_posts.csv": likes_received_for_posts_columns,
        "likes_received_from_users.csv": likes_received_from_users_columns,
        "likes_given_to_users.csv": likes_given_to_users_columns
    }

    df = pd.DataFrame(columns=columns_dic[name])
    abs_path = path.dirname(__file__) + '/csv_files/' + name
    df.to_csv(abs_path, index=False)


def check_csv_files_dir():
    from os import path

    folder_name = 'csv_files'
    cur_dir = path.dirname(__file__)
    check_dir = path.join(cur_dir, folder_name)

    if not path.isdir(check_dir):
        os.mkdir(check_dir)
        print(bcolors.OKGREEN + '+++ {} folder created'.format(folder_name))


def check_csv_files_dir_files():
    from os import path

    cur_dir = path.dirname(__file__)
    check_dir = cur_dir + '/csv_files/'
    FILENAMES = [
        'users.csv',
        'likes_given_to_posts.csv',
        'likes_given_to_users.csv',
        'likes_received_for_posts.csv',
        'likes_received_from_users.csv',
    ]

    files = os.listdir(check_dir)
    non_existent_files = []

    for filename in FILENAMES:
        if filename not in files:
            non_existent_files.append(filename)
            print(bcolors.FAIL + '--- {} does not exist'.format(filename))

    print(bcolors.ENDC)

    return non_existent_files


def erase_files():
    txt_files = [
        'account.txt',
        'likes_to_users.txt',
        'likes_received_for_posts.txt',
        'likes_given_to_posts.txt',
        'likes_from_users.txt',
        'badges.txt'
    ]

    for txt_file in txt_files:
        with open(txt_file, 'w') as f:
            f.write('')


def get_data(user_id):
    # make sure files and folders exist
    check_csv_files_dir()
    res = check_csv_files_dir_files()

    if len(res) > 0:
        for filename in res:
            create_csv_file(filename)
            print(bcolors.OKGREEN + '+++ {} created'.format(filename))

    print(bcolors.ENDC)

    try:

        erase_files()

        scraper = Scraper(
            user_id=user_id,
            users_columns=users_columns,
            likes_received_for_posts_columns=likes_received_for_posts_columns,
            likes_given_to_posts_columns=likes_given_to_posts_columns,
            likes_received_from_users_columns=likes_received_from_users_columns,  # noqa
            likes_given_to_users_columns=likes_given_to_users_columns
        )

        print('---Adding user---')
        user_data = scraper.add_to_user_csv()
        if user_data is True:
            util.write_timeout_id(user_id)
            return

        util.sleep()

        print('---Likes Received from users---')
        likes_received_from_users_data = scraper.get_likes_received_from_and_given_to_users(query_type="m")  # noqa
        if likes_received_from_users_data is True:
            util.write_timeout_id(user_id)
            return

        util.sleep()

        print('---Likes Given to users---')
        likes_given_to_users_data = scraper.get_likes_received_from_and_given_to_users(query_type="i")  # noqa
        if likes_given_to_users_data is True:
            util.write_timeout_id(user_id)
            return

        util.sleep()

        print('---Likes Received for posts---')
        like_received_for_posts_data = scraper.get_likes_received_for_posts()
        if like_received_for_posts_data is True:
            util.write_timeout_id(user_id)
            return

        util.sleep()

        print('---Likes Given to posts---')
        like_given_to_posts_data = scraper.get_likes_given_to_posts()
        if like_given_to_posts_data is True:
            util.write_timeout_id(user_id)
            return

        titles_arr = [
            users_columns,
            likes_given_to_posts_columns,
            likes_received_for_posts_columns,
            likes_given_to_users_columns,
            likes_received_from_users_columns,
        ]

        FILENAMES = [
            'users.csv',
            'likes_given_to_posts.csv',
            'likes_received_for_posts.csv',
            'likes_given_to_users.csv',
            'likes_received_from_users.csv',
        ]

        datas = [
            user_data,
            like_given_to_posts_data,
            like_received_for_posts_data,
            likes_given_to_users_data,
            likes_received_from_users_data
        ]

        def store_data(titles_arr, filenames, datas):
            for titles, filename, data in zip(titles_arr, filenames, datas):
                if data is not None:
                    new_data_df = pd.DataFrame(columns=titles, data=data)

                    FILEPATH = os.path.dirname(__file__)
                    FILEPATH += '/csv_files/' + filename
                    orig_df = pd.read_csv(FILEPATH)

                    result_df = pd.concat([orig_df, new_data_df])
                    result_df.to_csv(FILEPATH, index=False)

        store_data(titles_arr, FILENAMES, datas)

        return 'finished'
    except (AttributeError, ConnectionError, HTTPError) as err:
        return 'error: {}'.format(err)


ABS_PATH = os.path.dirname(__file__)

timeout_ids_filename = 'timeout_ids_2.txt'
timeout_ids_next_part_filename = 'timeout_ids_3.txt'

if timeout_ids_next_part_filename not in os.listdir(ABS_PATH):
    print(f'Creating {timeout_ids_next_part_filename}')
    with open(timeout_ids_next_part_filename, 'w') as f:
        f.write('')

with open(timeout_ids_filename, 'r') as f:
    for line in f:
        user_id = line[:-1]
        if user_id != 'Anonymous':
            try:
                print(f'*********{user_id}*********')
                get_data(int(user_id))
            except:
                print(f'*********{user_id} continuing*********')
                with open(timeout_ids_next_part_filename, 'a') as f:
                    content = f"{user_id}\n"
                    f.write(content)
