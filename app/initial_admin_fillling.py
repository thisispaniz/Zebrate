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
VALUES ('Zebrate', '$2a$12$Zl4XqePN/Qr7Wd3RgjKsJe58twIUIT1mdF2oktuNLZQd30Vk2rJQi'); """

delete_row = """
DELETE FROM admin WHERE id = 1;

"""

#cursor.execute(fill_admin)
cursor.execute(delete_row)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("filled the desired table successfully.")