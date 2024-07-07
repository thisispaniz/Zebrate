import sqlite3
from pathlib import Path

# Define the path to the app directory and database
app_path = Path(__file__).parent
db_path = app_path / 'venues.db'

# Connect to the database
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

fill_admin = """ 
INSERT INTO admin (username, password)
VALUES ('Zebrate', 'Zebrate-admin1234'); """

cursor.execute(fill_admin)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("filled the desired table successfully.")