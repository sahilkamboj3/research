class UtilClass(object):
    def __init__(self):
        pass

    def string_to_datetime(self, input_time):
        # input must be in this format : 08-02-2016 02:01 AM
        from datetime import datetime
        return datetime.strptime(input_time, "%m-%d-%Y %I:%M %p")  # returns military time for %I:%M %p # noqa

    def get_page_max(self, soup):
        page_max_ul = soup.find(
            'ul', {'class': 'lia-paging-full-pages'})
        if page_max_ul:
            last_li = page_max_ul.find(
                'li', {'class': 'lia-paging-page-last'})
            page_max = int(last_li.find('a').text)

            return page_max

        print('Page Max: ' + str(1))
        return 1

    def sleep(self):
        import time
        import random

        num = 0.25
        print(str(num) + ' sec')
        time.sleep(num)

    def is_id_valid(self, user_id):
        import pandas as pd
        from os import path

        try:
            ABS_PATH = path.dirname(__file__) + '/csv_files/users.csv'
            df = pd.read_csv(ABS_PATH)
            if user_id in df['id']:
                return False
        except FileNotFoundError:
            return True
        return True

    def write_timeout_id(user_id):
        filename = 'timeout_ids_2.txt'
        with open(filename, 'a') as f:
            content = f"{user_id}\n"
            f.write(content)
