#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator function to stream user records one at a time from the database"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',  # 🔒 Replace with your actual MySQL root password
            database='ALX_prodev'
        )
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            
            for row in cursor:
                yield row

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#!/usr/bin/python3
from itertools import islice
stream_users = __import__('0-stream_users').stream_users

# Print the first 6 rows from the generator
for user in islice(stream_users(), 6):
    print(user)
