#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator to stream users in batches of batch_size"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',  # 🔒 Replace with your real password
            database='ALX_prodev'
        )
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch  # Yield the whole batch as a list of rows

    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def batch_processing(batch_size):
    """Processes users in batches and yields only those older than 25"""
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user.get('age', 0) > 25:
                print(user)  # or yield user if needed


#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

try:
    for user in processing.batch_processing(50):
        print(user)
except BrokenPipeError:
    sys.stderr.close()

