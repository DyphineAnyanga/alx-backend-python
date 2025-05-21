import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.results = None

    def __enter__(self):
        # Open the database connection and execute the query
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the database connection
        if self.connection:
            self.connection.close()

# Usage Example:
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as result:
        for row in result:
            print(row)
