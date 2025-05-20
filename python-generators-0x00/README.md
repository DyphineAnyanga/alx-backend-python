## Getting Started with Python Generators

> Objective: Create a generator that streams rows from an SQL database one at a time.

### Instructions

- Create and connect to a MySQL database `ALX_prodev`.
- Create a table `user_data` with fields:
  - `user_id` (UUID, Primary Key)
  - `name` (VARCHAR)
  - `email` (VARCHAR)
  - `age` (DECIMAL)
- Populate the table from a CSV file (`user_data.csv`).
- Use a generator to stream data row by row.

### File: `seed.py`

Includes the following functions:

- `connect_db()`: Connects to the MySQL server.
- `create_database(connection)`: Creates the `ALX_prodev` database.
- `connect_to_prodev()`: Connects to `ALX_prodev`.
- `create_table(connection)`: Creates the `user_data` table.
- `insert_data(connection, csv_file)`: Seeds the table with data from CSV.

---

