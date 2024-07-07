import sqlite3
from pathlib import Path

# Define the path to the app directory and database
app_path = Path(__file__).parent
db_path = app_path / 'venues.db'

# Connect to the database
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# Function to check if a column exists
def column_exists(table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    return column_name in columns

# List of columns to add with their respective types
columns_to_add = [
    ("review_title", "TEXT"),
    ("colors", "INTEGER"),
    ("smells", "INTEGER"),
    ("quiet", "INTEGER"),
    ("crowdedness", "INTEGER"),
    ("food_variey", "INTEGER"),
    ("playground", "TEXT"),
    ("fenced", "TEXT"),
    ("quiet_zones", "TEXT"),
    ("food_own", "TEXT"),
    ("defined_duration", "TEXT")
]

# SQL command to create the 'users' table if it doesn't exist
create_users_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname TEXT,
    password TEXT
) """

# SQL command to create the 'reviews' table if it doesn't exist
create_reviews_sql = """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    venue_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (venue_id) REFERENCES venues (id)
) """

create_request_sql = """
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    new_venue_name TEXT NOT NULL,
    venue_review TEXT,
    venue_review_title TEXT,
    google_link TEXT,
    colors INTEGER,
    smells INTEGER,
    quiet INTEGER ,
    crowdedness INTEGER,
    food_variey INTEGER,
    playground TEXT,
    fenced TEXT,
    quiet_zones TEXT,
    food_own TEXT,
    defined_duration TEXT 
    )

"""
create_admin_table_sql = """
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
"""

# Execute the SQL commands to ensure tables exist
#cursor.execute(create_users_table_sql)
#cursor.execute(create_reviews_sql)
#cursor.execute(create_request_sql)
cursor.execute(create_admin_table_sql)

# Add the new columns if they do not already exist
for column_name, column_type in columns_to_add:
    if not column_exists("reviews", column_name):
        alter_table_sql = f"ALTER TABLE reviews ADD COLUMN {column_name} {column_type}"
        cursor.execute(alter_table_sql)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Created the desired table successfully.")
