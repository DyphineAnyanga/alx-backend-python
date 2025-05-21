import sqlite3
import functools

def with_db_connection(func):
    """Decorator to manage opening and closing the DB connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)

import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Alice'), (2, 'Bob')")
conn.commit()
conn.close()
