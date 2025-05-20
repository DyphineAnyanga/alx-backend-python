#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetches a page of users from the database with given offset and limit"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator that lazily loads each page of users"""
    offset = 0
    while True:  # one loop only
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination

try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()
