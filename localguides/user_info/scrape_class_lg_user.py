class Scraper(object):
    def __init__(
            self,
            user_id,
            users_columns,
            likes_received_for_posts_columns,
            likes_given_to_posts_columns,
            likes_received_from_users_columns,
            likes_given_to_users_columns
    ):

        from Util import UtilClass
        self.util = UtilClass()

        self.user_id = user_id
        self.name = None
        self.users_columns = users_columns
        self.likes_received_for_posts_columns = likes_received_for_posts_columns  # noqa
        self.likes_given_to_posts_columns = likes_given_to_posts_columns
        self.likes_received_from_users_columns = likes_received_from_users_columns  # noqa
        self.likes_given_to_users_columns = likes_given_to_users_columns

    def add_to_user_csv(self):
        import requests as re
        from bs4 import BeautifulSoup
        data = []

        BASE_URL = f'https://www.localguidesconnect.com/t5/user/viewprofilepage/user-id/{self.user_id}'

        try:
            res = re.get(BASE_URL, headers={}, timeout=10)
        except re.exceptions.Timeout as err:
            print("Timeout error")
#            #quit()
            return True

        with open('account.txt', 'w') as f:
            f.write(res.text)

        with open('account.txt') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        # soup = BeautifulSoup(res.text, 'html.parser')

        name = soup.find('span', {'class': 'user_login'}).text
        self.name = name

        level = soup.find('div', {'class': 'user_rank'}).text
        total_posts = soup.find(
            'td', {'class': 'messagesPosted'}).text.rstrip().lstrip()

        likes_received_and_given = soup.find_all('td', {'class': 'kudosReceived'})  # noqa
        if len(likes_received_and_given) == 1:
            total_likes_received = 0
            total_likes_given = int(likes_received_and_given[0].text)
        else:
            total_likes_received = int(likes_received_and_given[0].text)
            total_likes_given = int(likes_received_and_given[1].text)

        bio_tag = soup.find('div', {'class': 'bio'})
        bio = bio_tag.text if bio_tag else "None"

        total_badges, badges = self._get_user_badges()

        data_row = [
            self.user_id,
            name,
            level,
            total_posts,
            total_likes_received,
            total_likes_given,
            bio,
            total_badges,
            badges  # tuples
        ]
        data.append(data_row)

        return data

    def _get_user_badges(self):
        def compare_texts(text1, text2):
            import difflib
            diffs = difflib.ndiff(text1, text2)

            for i, s in enumerate(diffs):
                if s[0] == ' ':
                    continue
                elif s[0] == '-':
                    print(u'Delete "{}" from position {}'.format(s[-1], i))
                elif s[0] == '+':
                    print(u'Add "{}" to position {}'.format(s[-1], i))

        import requests as re
        from bs4 import BeautifulSoup

        page = 1
        badges = []

        try:
            BASE_URL = f'https://www.localguidesconnect.com/t5/badges/userbadgespage/user-id/{self.user_id}/page/{page}'
            try:
                res = re.get(BASE_URL, headers={}, timeout=10)
            except re.exceptions.Timeout as err:
                print("Timeout error")
                # quit()
                return True

            with open('badges.txt', 'w') as f:
                f.write(res.text)

            with open('badges.txt', 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            badge_names_tags = soup.find_all(
                'div', {'class', 'lia-user-badge-name'})
            badge_date_tags = soup.find_all(
                'span', {'class', 'local-date'})
            badge_earned_by_tags = soup.find_all(
                'div', {'class', 'lia-badge-participants-count'})

            if len(badge_date_tags) > 0:
                for name_tag, date_tag, earned_by_tag in zip(badge_names_tags, badge_date_tags, badge_earned_by_tags):  # noqa
                    name = name_tag.text.lstrip().rstrip()
                    date = date_tag.text.strip('\u200e')

                    earned_by_text = earned_by_tag.text.lstrip().rstrip()
                    last_space_idx = earned_by_text.rfind(' ')
                    earned_by_input = earned_by_text[last_space_idx + 1:]
                    earned_by = int(earned_by_input.replace(',', ''))

                    badge_tuple = ((name, earned_by, date))
                    badges.append(badge_tuple)
        except:
            return len(badges), badges

        return len(badges), badges

    def get_likes_received_from_and_given_to_users(self, query_type):
        import requests as re
        from bs4 import BeautifulSoup

        page = page_max = 1
        data = []

        while page <= page_max:
            # print("Page Num: {}, Page Max: {}".format(page, page_max))

            if query_type == "i":
                # if page == 1:
                #     url = f'https://www.localguidesconnect.com/t5/kudos/userpage/user-id/{self.user_id}/tab/users-i-kudoed'  # noqa
                #     print(url)
                # else:
                url = f'https://www.localguidesconnect.com/t5/kudos/userpage/user-id/{self.user_id}/tab/users-i-kudoed/page/{page}'  # noqa

                try:
                    res = re.get(url, headers={}, timeout=10)
                except re.exceptions.Timeout as err:
                    print("Timeout error")
                    # quit()
                    return True

                with open('likes_to_users.txt', 'w') as f:
                    f.write(res.text)

                with open('likes_to_users.txt', 'r') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
            else:
                # if page == 1:
                #     url = f'https://www.localguidesconnect.com/t5/kudos/userpage/user-id/{self.user_id}/tab/users-who-kudoed'  # noqa
                #     print(url)
                # else:
                url = f'https://www.localguidesconnect.com/t5/kudos/userpage/user-id/{self.user_id}/tab/users-who-kudoed/page/{page}'  # noqa
                try:
                    res = re.get(url, headers={}, timeout=10)
                except re.exceptions.Timeout as err:
                    print("Timeout error")
                    # quit()
                    return True

                with open('likes_from_users.txt', 'w') as f:
                    f.write(res.text)

                with open('likes_from_users.txt', 'r') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')

            if page == 1:
                page_max = self.util.get_page_max(soup)

            user_name_div_tags = soup.find_all(
                'a', {'class': 'lia-user-name-link'})
            user_level_tags = soup.find_all('div', {'class': 'lia-user-rank'})
            like_tags = soup.find_all('span', {'class': 'base-count-number'})

            if user_name_div_tags is not None:
                for user_name_div_tag, user_level_tag, like_tag in zip(user_name_div_tags, user_level_tags, like_tags):  # noqa
                    name = user_name_div_tag.find('span').text
                    url = user_name_div_tag['href']
                    user_id = int(url[url.rfind('/') + 1:])
                    level = user_level_tag.text
                    likes = int(like_tag.text)

                    data.append([
                        self.user_id,
                        self.name,
                        name,
                        user_id,
                        url,
                        level,
                        likes
                    ])

            page += 1
            self.util.sleep()

        return data

    def get_likes_received_for_posts(self):
        import requests as re
        from bs4 import BeautifulSoup

        data = []
        page = page_max = 1

        while page <= page_max:
            # print("Page Num: {}, Page Max: {}".format(page, page_max))

            BASE_URL = f'https://www.localguidesconnect.com/t5/kudos/userpage/user-id/{self.user_id}/tab/my-kudoed-messages/page/{page}'
            try:
                res = re.get(BASE_URL, headers={}, timeout=10)
            except re.exceptions.Timeout as err:
                print("Timeout error")
                # quit()
                return True

            with open('likes_received_for_posts.txt', 'w') as f:
                f.write(res.text)

            with open('likes_received_for_posts.txt', 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            if page == 1:
                page_max = self.util.get_page_max(soup)

            post_title_tags = soup.find_all(
                'a', {'class': 'page-link'})
            reply_tags = soup.find_all(
                'td', {'class': 'repliesCountColumn'})
            like_tags = soup.find_all('span', {'class': 'MessageKudosCount'})
            dates_posted_tags = soup.find_all('span', {'class': 'local-date'})
            times_posted_tags = soup.find_all('span', {'class': 'local-time'})
            post_type_tags = soup.find_all('a', {'class': 'xsmall-text'})
            icon_tags = soup.find_all('div', {'class', 'MessageSubjectIcons'})

            if post_title_tags is not None:
                for i in range(len(post_title_tags)):
                    post_title = post_title_tags[i].text.lstrip().rstrip()
                    total_replies = int(reply_tags[i].text)
                    total_likes = int(like_tags[i].text)
                    post_type = post_type_tags[i].text

                    icons = []
                    icon_tag = icon_tags[i]
                    icon_span_tags = icon_tag.find_all(
                        'span', {'class', 'lia-fa-message'})

                    if len(icon_span_tags) > 0:
                        for span in icon_span_tags:
                            icon_alt_property = span['alt']
                            last_space_idx = icon_alt_property.rfind(' ')
                            icons.append(
                                icon_alt_property[last_space_idx + 1:])

                    date = dates_posted_tags[i].text.lstrip().rstrip()
                    time = times_posted_tags[i].text.lstrip().rstrip()
                    input_time = date + ' ' + time
                    input_time = input_time.strip('\u200e')
                    date_posted = self.string_to_datetime(input_time)

                    data.append([
                        self.user_id,
                        self.name,
                        post_title,
                        post_type,
                        total_replies,
                        total_likes,
                        icons,
                        date_posted
                    ])

            # else:
            #     data = None
            page += 1
            self.util.sleep()

        return data

    def get_likes_given_to_posts(self):
        import requests as re
        from bs4 import BeautifulSoup
        data = []
        page = page_max = 1

        while page <= page_max:
            BASE_URL = f'https://www.localguidesconnect.com/t5/kudos/userpage/user-id/{self.user_id}/tab/messages-kudoed-by-user/page/{page}'

            try:
                res = re.get(BASE_URL, headers={}, timeout=10)
            except re.exceptions.Timeout as err:
                print("Timeout error")
                # quit()
                return True

            with open('likes_given_to_posts.txt', 'w') as f:
                f.write(res.text)

            with open('likes_given_to_posts.txt', 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            if page == 1:
                page_max = self.util.get_page_max(soup)

            post_title_tags = soup.find_all(
                'a', {'class': 'page-link'})
            reply_tags = soup.find_all(
                'td', {'class': 'repliesCountColumn'})
            like_tags = soup.find_all('span', {'class': 'MessageKudosCount'})
            dates_posted_tags = soup.find_all('span', {'class': 'local-date'})
            times_posted_tags = soup.find_all('span', {'class': 'local-time'})
            # authors_tags = soup.find_all(
            #     'a', {'class': 'lia-user-name-link'})
            authors_tags = soup.find_all(
                'span', {'class': 'lia-user-name'})
            post_type_tags = soup.find_all('a', {'class': 'xsmall-text'})
            icon_tags = soup.find_all('div', {'class', 'MessageSubjectIcons'})

            if post_title_tags is not None:
                for i in range(len(post_title_tags)):
                    post_title = post_title_tags[i].text.lstrip().rstrip()
                    total_replies = int(reply_tags[i].text)
                    total_likes = int(like_tags[i].text.replace(
                        '\t', '').replace('\n', '').replace(',', ''))
                    post_type = post_type_tags[i].text

                    icons = []
                    icon_tag = icon_tags[i]
                    icon_span_tags = icon_tag.find_all(
                        'span', {'class', 'lia-fa-message'})

                    if len(icon_span_tags) > 0:
                        for span in icon_span_tags:
                            icon_alt_property = span['alt']
                            last_space_idx = icon_alt_property.rfind(' ')
                            icons.append(
                                icon_alt_property[last_space_idx + 1:])

                    date = dates_posted_tags[i].text
                    time = times_posted_tags[i].text
                    input_time = date + ' ' + time
                    input_time = input_time.strip('\u200e')
                    date_posted = self.string_to_datetime(input_time)

                    if authors_tags[i].find('a'):
                        author = authors_tags[i].find('a').find('span').text
                        author_url = authors_tags[i].find('a')['href']
                        last_slash_idx = author_url.rfind('/')
                        author_id = int(author_url[last_slash_idx + 1:])
                    else:
                        author = "Anonymous"
                        author_url = "None"
                        author_id = "None"

                    data.append([
                        self.user_id,
                        self.name,
                        author,
                        author_url,
                        author_id,
                        post_title,
                        post_type,
                        total_replies,
                        total_likes,
                        icons,
                        date_posted
                    ])
            # else:
            #     data = None
            page += 1
            self.util.sleep()

        return data

    def string_to_datetime(self, input_time):
        # input must be in this format : 08-02-2016 02:01 AM
        from datetime import datetime
        return datetime.strptime(input_time, "%m-%d-%Y %I:%M %p")  # returns military time for %I:%M %p # noqa
