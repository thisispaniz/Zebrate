"""

import sqlite3
from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from passlib.context import CryptContext
from datetime import datetime
import os

app = FastAPI()

# Define the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Connect to SQLite database
conn = sqlite3.connect(os.path.join(BASE_DIR, 'data.db'), check_same_thread=False)
conn.row_factory = sqlite3.Row  # Allows accessing columns by name
c = conn.cursor()

# Create tables if they don't exist
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
             individual_play TEXT,
             other_concerns TEXT,
             timestamp TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             username TEXT UNIQUE,
             hashed_password TEXT)''')

conn.commit()
conn.close()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@app.get("/", response_class=FileResponse)
def get_html():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/signup", response_class=FileResponse)
def get_signup():
    return FileResponse(os.path.join(BASE_DIR, "signup.html"))

@app.get("/login", response_class=FileResponse)
def get_login():
    return FileResponse(os.path.join(BASE_DIR, "login.html"))

@app.get("/survey", response_class=FileResponse)
def get_survey():
    return FileResponse(os.path.join(BASE_DIR, "Survey.html"))

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
    playgrounds: str = Form(...),
    individual_play: str = Form(...),
    other_concerns: str = Form(...)
):
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(os.path.join(BASE_DIR, 'data.db'), check_same_thread=False) as conn:
        conn.execute('''INSERT INTO survey_responses (
                        main_challenges, quiet_zone, noise_sensitivity, sensory_issues, 
                        crowd_tolerance, animals, restrict_noise, food_options, playgrounds, 
                        individual_play, other_concerns, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (main_challenges, quiet_zone, noise_sensitivity, sensory_issues, 
                      crowd_tolerance, animals, restrict_noise, food_options, playgrounds, 
                      individual_play, other_concerns, current_timestamp))
        conn.commit()

    return RedirectResponse(url="/thankyou.html", status_code=303)

@app.get("/view-results/")
async def view_results():
    with sqlite3.connect(os.path.join(BASE_DIR, 'data.db'), check_same_thread=False) as conn:
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM survey_responses")
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
    return JSONResponse(content=results)

# User management
@app.post("/register/")
async def register(username: str = Form(...), password: str = Form(...)):
    hashed_password = get_password_hash(password)
    with sqlite3.connect(os.path.join(BASE_DIR, 'data.db'), check_same_thread=False) as conn:
        try:
            conn.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)',
                         (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Username already registered")
    return {"message": "User registered successfully"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with sqlite3.connect(os.path.join(BASE_DIR, 'data.db'), check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (form_data.username,))
        user = cursor.fetchone()
        if not user or not verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return {"access_token": user["username"], "token_type": "bearer"}
"""