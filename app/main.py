import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
from pathlib import Path
from fastapi import Form
from passlib.hash import bcrypt
import logging
from fastapi import HTTPException

app = FastAPI()

# Define the path to the app directory
app_path = Path(__file__).parent

# Serve the entire app directory as static files
app.mount("/static", StaticFiles(directory=app_path, html=True), name="static")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection to venues.db
db_path = app_path / 'venues.db'

@app.get("/", response_class=HTMLResponse)
def get_index():
    """
    Serves the index.html file at the root path.
    """
    return FileResponse(app_path / "index.html")

@app.get("/discover", response_class=HTMLResponse)
async def get_discover():
    """
    Fetches and displays all venues from the database.
    """
    try:
        # Connect to the database and retrieve all venues
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row  # Access columns by name
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM venues")
            venues = cursor.fetchall()  # Fetch all venues

        # Load the discover.html template and render it with the list of venues
        template_path = app_path / "discover.html"
        with open(template_path, "r") as file:
            template = Template(file.read())

        rendered_html = template.render(venues=venues, query="")
        return HTMLResponse(content=rendered_html)

    except Exception as e:
        logger.error(f"Error loading discover page: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)

@app.get("/signup", response_class=HTMLResponse)
def get_signup():
    """
    Serves the signup.html file for user registration.
    """
    return FileResponse(app_path / "signup.html")

@app.get("/search-venues/", response_class=HTMLResponse)
async def search_venues(request: Request):
    query = request.query_params.get('query', '')

    # Determine the SQL query to use based on the presence of the search query
    if query:
        sql_query = """
            SELECT * FROM venues WHERE
            name LIKE ? OR
            address LIKE ? OR
            playground LIKE ? OR
            fenced LIKE ? OR
            quiet_zones LIKE ? OR
            colors LIKE ? OR
            smells LIKE ? OR
            food_own LIKE ? OR
            defined_duration LIKE ? OR
            photo_url LIKE ?
        """
        parameters = [f"%{query}%"] * 10  # Apply the search term to all fields
        
    else:
        sql_query = "SELECT * FROM venues"
        parameters = []  # No parameters needed for a full table query

    # Connect to the database and execute the query
    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query, parameters)
        venues = cursor.fetchall()

    # Load the template and render it with the search results and the query term
    template_path = app_path / "results.html"
    with open(template_path, "r") as file:
        template = Template(file.read())

    rendered_html = template.render(venues=venues, query=query)
    return HTMLResponse(content=rendered_html)


@app.get("/filter-venues/", response_class=HTMLResponse)
async def filter_venues(
    request: Request,
    playground: str = None,
    fenced: str = None,
    quiet_zones: str = None,
    colors: str = None,
    smells: str = None,
    food_own: str = None,
    defined_duration: str = None,
    quiet: str = None,
    crowdedness: str = None,
    food_variety: str = None
):
    """
    Handles detailed filtering of venues based on user-selected criteria.
    If no filter options are provided, select all entries.
    """
    filters = {
        "playground": playground,
        "fenced": fenced,
        "quiet_zones": quiet_zones,
        "colors": colors,
        "smells": smells,
        "food_own": food_own,
        "defined_duration": defined_duration,
        "quiet": quiet,
        "crowdedness": crowdedness,
        "food_variety": food_variety
    }

    # Start with the base query
    query = "SELECT * FROM venues WHERE 1=1"
    parameters = []

    # Append conditions based on provided filter values
    for key, value in filters.items():
        if value:
            query += f" AND {key} LIKE ?"
            parameters.append(f"%{value}%")

    try:
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            venues = cursor.fetchall()

        # Load the results.html template and render it with the filtered results
        template_path = app_path / "results.html"
        with open(template_path, "r") as file:
            template = Template(file.read())

        rendered_html = template.render(venues=venues, filters=filters)
        return HTMLResponse(content=rendered_html)

    except Exception as e:
        logger.error(f"Error filtering venues: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)

@app.get("/venue/{venue_id}", response_class=HTMLResponse)
async def get_venue(venue_id: int):
    """
    Retrieve and display details for a specific venue based on its ID.
    """
    try:
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row  # Access columns by name
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM venues WHERE id = ?", (venue_id,))
            venue = cursor.fetchone()  # Fetch the venue details

        if venue is None:
            return HTMLResponse(content="Venue not found", status_code=404)

        # Convert the sqlite3.Row object to a dictionary for easier handling in the template
        venue_dict = dict(venue)

        # Render the template with venue details
        template_path = app_path / "venue_page.html"
        with open(template_path, "r") as file:
            template = Template(file.read())

        rendered_html = template.render(venue=venue_dict)
        return HTMLResponse(content=rendered_html)

    except Exception as e:
        return HTMLResponse(content=f"An unexpected error occurred {e}", status_code=500)



@app.post("/register/")
async def register_user(nickname: str = Form(...), password: str = Form(...)):
    try:
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            cursor = conn.cursor()

            # Check if the nickname already exists
            cursor.execute("SELECT * FROM users WHERE nickname = ?", (nickname,))
            existing_user = cursor.fetchone()

            if existing_user:
                logger.info(f"Nickname {nickname} already taken.")
                return HTMLResponse(content="nickname already taken", status_code=400)

            # Hash the password for security
            hashed_password = bcrypt.hash(password)

            # Insert the new user into the database
            cursor.execute("INSERT INTO users (nickname, password) VALUES (?, ?)", (nickname, hashed_password))
            conn.commit()

            logger.info(f"User {nickname} registered successfully.")
            # Redirect to the login page after successful registration
            return RedirectResponse(url="/static/login.html", status_code=303)

    except Exception as e:
        logger.error(f"Registration error: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)

@app.get("/login", response_class=HTMLResponse)
def get_login():
    """
    Serves the login.html file for user login.
    """
    return FileResponse(app_path / "login.html")

@app.post("/login/")
async def login_user(nickname: str = Form(...), password: str = Form(...)):
    try:
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Check if the nickname exists
            cursor.execute("SELECT * FROM users WHERE nickname = ?", (nickname,))
            user = cursor.fetchone()

            if not user:
                logger.info(f"Invalid login attempt for nickname {nickname}.")
                return HTMLResponse(content="Invalid nickname or password", status_code=400)

            # Verify the password
            if not bcrypt.verify(password, user["password"]):
                logger.info(f"Invalid password for nickname {nickname}.")
                return HTMLResponse(content="Invalid nickname or password", status_code=400)
            

            logger.info(f"User {nickname} logged in successfully.")
            # Redirect to the dashboard with the user's nickname
            return RedirectResponse(url=f"/welcome?nickname={nickname}", status_code=303)

            

    except Exception as e:
        logger.error(f"Login error: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)


@app.get("/welcome", response_class=HTMLResponse)
async def get_welcome(request: Request):
    """
    Serves the welcome page after successful login.
    Includes a form to add reviews and lists submitted reviews.
    """
    try:
        nickname = request.query_params.get('nickname')
        if not nickname:
            return HTMLResponse(content="Nickname not found in the request", status_code=400)

        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Fetch all reviews to display on the welcome page
            cursor.execute("""
                SELECT reviews.review_text, reviews.timestamp, users.nickname, venues.name AS venue_name
                FROM reviews
                JOIN users ON reviews.user_id = users.id
                JOIN venues ON reviews.venue_id = venues.id
                ORDER BY reviews.timestamp DESC
            """)
            reviews = cursor.fetchall()

            # Fetch all venues to populate the dropdown
            cursor.execute("SELECT id, name FROM venues")
            venues = cursor.fetchall()

        # Load dashboard.html template and render it with the reviews and venues data
        template_path = app_path / "dashboard.html"
        with open(template_path, "r") as file:
            template = Template(file.read())

        rendered_html = template.render(reviews=reviews, venues=venues, nickname=nickname)
        return HTMLResponse(content=rendered_html)

    except Exception as e:
        logger.error(f"Error loading welcome page: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)



# Serve the entire app directory as static files
app.mount("/static", StaticFiles(directory=app_path, html=True), name="static")
