
import sqlite3
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect('data.db', check_same_thread=False)
conn.row_factory = sqlite3.Row  # Allows accessing columns by name
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS survey_responses (
             id INTEGER PRIMARY KEY,
             main_challenges TEXT,
             quiet_zone TEXT,
             noise_sensitivity TEXT,
             sensory_issues TEXT,
             crowd_tolerance TEXT,
             animals TEXT,
             restrict_noise TEXT,
             food_options TEXT,
             playgrounds TEXT,
             timestamp TEXT)''')
conn.commit()
conn.close()

@app.get("/", response_class=FileResponse)
def get_html():
    return FileResponse("Survey.html")

@app.post("/submit-survey/")
async def submit_survey(
    main_challenges: str = Form(...),
    quiet_zone: str = Form(...),
    noise_sensitivity: str = Form(...),
    sensory_issues: str = Form(...),
    crowd_tolerance: str = Form(...),
    animals: str = Form(...),
    restrict_noise: str = Form(...),
    food_options: str = Form(...),
    playgrounds: str = Form(...)
):
    # Get current timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert survey responses into database
    with sqlite3.connect('data.db', check_same_thread=False) as conn:
        conn.execute('''INSERT INTO survey_responses (
                        main_challenges, quiet_zone, noise_sensitivity, sensory_issues, 
                        crowd_tolerance, animals, restrict_noise, food_options, playgrounds, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (main_challenges, quiet_zone, noise_sensitivity, sensory_issues, 
                      crowd_tolerance, animals, restrict_noise, food_options, playgrounds, current_timestamp))
        conn.commit()

    return RedirectResponse(url="/static/thankyou.html", status_code=303)

@app.get("/view-results/")
async def view_results():
    with sqlite3.connect('data.db', check_same_thread=False) as conn:
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM survey_responses")
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
    return JSONResponse(content=results)

# Mount the folder to make files accessible
app.mount("/static", StaticFiles(directory="./"), name="static")