import sqlite3
from pathlib import Path

# Define the path to the app directory and database
app_path = Path(__file__).parent
db_path = app_path / 'venues.db'

# Connect to the database
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# SQL command to create the 'users' table if it doesn't exist
create_users_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT,
    password TEXT
) """

# Execute the SQL command
cursor.execute(create_users_table_sql)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Created the users' table successfully.")
