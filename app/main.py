from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
from datetime import datetime

app = FastAPI()



# Connect to SQLite database
conn = sqlite3.connect('data.db', check_same_thread=False)
conn.row_factory = sqlite3.Row  # Allows accessing columns by name
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS timestamps
             (id INTEGER PRIMARY KEY, timestamp TEXT)''')
conn.commit()

# Close the connection
conn.close()

@app.get("/", response_class=FileResponse)
def get_html():
    return FileResponse("index.html")

@app.post("/submit/")
async def submit_timestamp(request: Request):
    # Get current timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert timestamp into database
    with sqlite3.connect('data.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO timestamps (timestamp) VALUES (?)", (current_timestamp,))
        conn.commit()

    return RedirectResponse(url="/otherpage.html", status_code=303)

# Mount the folder to make files accessible
app.mount("/", StaticFiles(directory="./"), name="static")
