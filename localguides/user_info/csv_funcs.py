import pandas as pd
from os import path
import os


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


titles_arr = [
    users_columns,
    likes_given_to_posts_columns,
    likes_received_for_posts_columns,
    likes_given_to_users_columns,
    likes_received_from_users_columns,
]

FILENAMES_checkpoint = {
    'users.csv': 'id',
    'likes_given_to_posts.csv': 'id',
    'likes_received_for_posts.csv': 'id',
    'likes_given_to_users.csv': 'from_id',
    'likes_received_from_users.csv': 'to_id',
}


def df_drop_duplicates():
    ABS_PATH = path.dirname(__file__)
    for filename in FILENAMES_checkpoint:
        ABS_PATH = path.dirname(__file__) + '/csv_files/' + filename
        df = pd.read_csv(ABS_PATH)
        print(filename)
        print("old: ", len(df))
        new_df = df.drop_duplicates()
        print("new: ", len(new_df))
        new_df.to_csv(ABS_PATH, index=False)


def print_file_lengths():
    ABS_PATH = path.dirname(__file__)
    for filename in FILENAMES_checkpoint:
        ABS_PATH = path.dirname(__file__) + '/csv_files/' + filename
        df = pd.read_csv(ABS_PATH)
        print(f"{filename}: {len(df)}")


def get_users_csv_length():
    for filename in FILENAMES_checkpoint:
        if filename == 'users.csv':
            ABS_PATH = path.dirname(__file__) + '/csv_files/' + filename
            df = pd.read_csv(ABS_PATH)
            print("users.csv: ", len(df))


def get_timeout_txt_length():
    count = 0
    filename = 'timeout_ids_3.txt'

    with open(filename, 'r') as f:
        for line in f:
            content = line[:-1]
            if content != 'Anonymous':
                count += 1

    print("Timeout errors: ", count)


def check_uniques_txt_files():
    print("here")
    seen = {}
    filename = 'timeout_ids_3.txt'

    with open(filename, 'r') as f:
        for line in f:
            content = line[:-1]
            if content != 'Anonymous':
                if content not in seen:
                    #                    print(f"{content} unique")
                    seen[content] = 1
                else:
                    print(f"{content} duplicated")


# get_timeout_txt_length()
# print_file_lengths()
# df_drop_duplicates()
check_uniques_txt_files()
