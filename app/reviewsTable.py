import sqlite3
from pathlib import Path

# Define the path to the app directory and database
app_path = Path(__file__).parent
db_path = app_path / 'venues.db'

# Connect to the database
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# Drop the existing 'reviews' table
cursor.execute("DROP TABLE IF EXISTS reviews")

# Recreate the 'reviews' table without the 'user_id' column and its foreign key
create_reviews_table_sql = """
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    review_title TEXT,
    colors INTEGER,
    smells INTEGER,
    quiet INTEGER,
    crowdedness INTEGER,
    food_variey INTEGER,
    playground TEXT,
    fenced TEXT,
    quiet_zones TEXT,
    food_own TEXT,
    defined_duration TEXT,
    FOREIGN KEY (venue_id) REFERENCES venues (id)
) """

# Execute the SQL command to recreate the table
cursor.execute(create_reviews_table_sql)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Removed 'user_id' column and recreated the 'reviews' table successfully.")
