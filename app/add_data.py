import sqlite3
from pathlib import Path

# Define the path to the app directory and database
app_path = Path(__file__).parent
db_path = app_path / 'venues.db'

# Connect to the database
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# SQL command to create the 'venues' table if it doesn't exist
create_table_sql = """
CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    playground TEXT,
    fenced TEXT,
    quiet_zones TEXT,
    colors TEXT,
    smells TEXT,
    food_own TEXT,
    defined_duration TEXT
);
"""

# Execute the SQL command
cursor.execute(create_table_sql)

# SQL commands to insert sample data
insert_data_sql = """
INSERT INTO venues (name, address, photo_url, playground, fenced, quiet_zones, colors, smells, food_own, defined_duration, quiet, crowdedness, food_variey)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Sample data
sample_data = [
    ('Adventure Park Voglsam', 'Voglsam 1, 84337 Schönau', 'https://lh3.googleusercontent.com/p/AF1QipN_opfkihmBL6fqWUn8cgbjpanA3yGM0NPqRT0D=s680-w680-h510', "yes", "no", "yes", 1, 0, "yes", "no", 3, 3, 4),
    ('Bowling-Center Pfarrkirchen', 'Bahnweg 11 A, 84347 Pfarrkirchen', 'https://lh3.googleusercontent.com/p/AF1QipMtaA0fkL4_efmTy3-Lc78gbPhSVQDdbnbcHUUA=s680-w680-h510', "yes", "no", "no", 1, 1, "no", "no", 3, 2, 4)
]

# Insert the sample data into the database
for entry in sample_data:
    cursor.execute(insert_data_sql, entry)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Sample data inserted successfully.")
