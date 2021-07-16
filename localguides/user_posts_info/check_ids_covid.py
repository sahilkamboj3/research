import pandas as pd

covid_users_rel_path = '../../data/covid/users.csv'
covid_user_posts_rel_path = '../../data/user_posts_info/covid_user_posts_second.csv'

covid_users_df = pd.read_csv(covid_users_rel_path)
covid_users_posts_df = pd.read_csv(covid_user_posts_rel_path)


"""
count = 0
for id in covid_users_df['id']:
    count += 1
    is_in_posts = False
    if id in covid_users_posts_df['id']:
        is_in_posts = True
        print(f'{id}:{is_in_posts}')
    print(f'{id}:{is_in_posts}')

print()
print(count)
"""

print(len(covid_users_df))
covid_users_df.drop_duplicates(keep='first', inplace=True)
print(len(covid_users_df))

print(len(covid_users_posts_df))
covid_users_posts_df.drop_duplicates(keep='first', inplace=True)
print(len(covid_users_posts_df))

covid_users = set()
covid_users_posts = set()

for id in covid_users_df['id']:
    covid_users.add(id)
for id in covid_users_posts_df['id']:
    covid_users_posts.add(id)
