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

create_reviews = """ CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    venue_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (venue_id) REFERENCES venues (id)
) """

# Execute the SQL command
cursor.execute(create_users_table_sql)
cursor.execute(create_reviews)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Created the users' table and the reviews' table successfully.")
