#!/bin/bash
cd ../../ && . env/bin/activate && cd localguides/user_posts_info
python3 get_trending_user_ids.py
python3 sel_test.py 1 && python3 sel_test.py 2 && python3 sel_test.py 3
