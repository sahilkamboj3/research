import pandas as pd

# control_users_rel_path = '../../data/control/users.csv'
control_user_posts_rel_path = '../../data/user_posts_info/control_user_posts.csv'

# control_users_df = pd.read_csv(control_users_rel_path)
control_users_posts_df = pd.read_csv(control_user_posts_rel_path)

print(control_users_posts_df['id'].unique())
print(len(control_users_posts_df['id'].unique()))

print(len(control_users_posts_df))
two = control_users_posts_df.drop_duplicates(keep='first')
print(len(two))


"""
count = 0
for id in control_users_df['id']:
    count += 1
    is_in_posts = False
    if id in control_users_posts_df['id']:
        is_in_posts = True
        print(f'{id}:{is_in_posts}')
    print(f'{id}:{is_in_posts}')

print()
print(count)
"""

"""
print(len(control_users_df))
control_users_df.drop_duplicates(keep='first', inplace=True)
print(len(control_users_df))

print(len(control_users_posts_df))
control_users_posts_df.drop_duplicates(keep='first', inplace=True)
print(len(control_users_posts_df))

control_users = set()
control_users_posts = set()

for id in control_users_df['id']:
    control_users.add(id)
for id in control_users_posts_df['id']:
    control_users_posts.add(id)
"""
