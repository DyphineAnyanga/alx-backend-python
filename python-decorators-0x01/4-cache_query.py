import time
import sqlite3
import functools

# Simple in-memory cache
query_cache = {}

# Reusing with_db_connection from previous tasks
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Cache decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Assuming the first positional argument after conn is the query string
        query = kwargs.get("query") if "query" in kwargs else args[0]
        
        if query in query_cache:
            print("Using cached result.")
            return query_cache[query]
        
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("Query result cached.")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

