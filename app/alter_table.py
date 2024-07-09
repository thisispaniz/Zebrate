import sqlite3
import logging

# Configure logging
logging.basicConfig(filename='alter_table.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Define the path to your database
db_path = "venues.db"

def add_email_column():
    logging.debug("Starting the add_email_column function.")
    try:
        # Connect to the SQLite database
        logging.debug(f"Connecting to the SQLite database at {db_path}.")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if the 'users' table exists
        logging.debug("Checking if the 'users' table exists.")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not cursor.fetchone():
            logging.error("Table 'users' does not exist.")
            return

        # Check if the 'email' column already exists
        logging.debug("Checking if the 'email' column already exists in the 'users' table.")
        cursor.execute("PRAGMA table_info(users);")
        columns = [column[1] for column in cursor.fetchall()]
        if 'email' in columns:
            logging.info("Column 'email' already exists in the 'users' table.")
            return

        # Add the email column to the users table
        logging.debug("Adding the 'email' column to the 'users' table.")
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT;")
        conn.commit()
        logging.info("Email column added successfully.")

    except sqlite3.OperationalError as e:
        logging.error(f"An operational error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        logging.debug("Closing the database connection.")
        conn.close()

if __name__ == "__main__":
    add_email_column()
