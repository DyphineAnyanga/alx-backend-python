import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from arguments if it's passed as a keyword argument
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else 'UNKNOWN QUERY'
        print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)

import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie')")
conn.commit()
conn.close()
