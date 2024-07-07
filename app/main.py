import sqlite3
from fastapi import FastAPI, Request, Form, Depends, Cookie
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
from pathlib import Path
from passlib.hash import bcrypt
import logging
from fastapi import HTTPException
from typing import Optional
import json
from sqlite3 import connect
import os
from fastapi import Query

app = FastAPI()

# Define the path to the app directory
app_path = Path(__file__).parent


def render_template(template_name: str, **context):
    with open(os.path.join('templates', template_name)) as file_:
        template = Template(file_.read())
    return template.render(**context)


# Serve the entire app directory as static files
app.mount("/static", StaticFiles(directory=app_path, html=True), name="static")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection to venues.db
db_path = app_path / 'venues.db'


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.cookies.get("user")
    content = render_template(app_path / "index.html", user=user)
    return HTMLResponse(content=content)


@app.post("/add-review/")
async def add_review(
        venue_id: int = Form(...),
        review_title: str = Form(...),
        review_text: str = Form(...),
        colors: int = Form(...),
        smells: int = Form(...),
        quiet: int = Form(...),
        crowdedness: int = Form(...),
        food_variey: int = Form(...),
        playground: str = Form(...),
        fenced: str = Form(...),
        quiet_zones: str = Form(...),
        food_own: str = Form(...),
        defined_duration: str = Form(...),
        user: str = Cookie(None)
):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Insert the review into the database
        cursor.execute("""
            INSERT INTO reviews (
                venue_id, review_title, review_text, colors, smells, quiet, crowdedness, 
                food_variey, playground, fenced, quiet_zones, food_own, defined_duration, nickname
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            venue_id, review_title, review_text, colors, smells, quiet, crowdedness,
            food_variey, playground, fenced, quiet_zones, food_own, defined_duration, user
        ))

        # Commit the transaction
        conn.commit()

        # Return a success message
        return {"message": "Review added successfully!"}

    except sqlite3.Error as e:
        conn.rollback()  # Rollback the transaction on error
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        # Close the connection
        conn.close()
        # Redirect to the venue page with the added review
        return RedirectResponse(url=f"/venue/{venue_id}", status_code=303)


@app.get("/discover", response_class=HTMLResponse)
async def get_discover(request: Request, query: str = None, filters: str = None):
    try:
        venues = fetch_venues(query, filters)
        with open("discover.html", "r") as file:
            template = Template(file.read())
            user = request.cookies.get("user")
        rendered_html = template.render(venues=venues, query=query or "", filters=filters or "{}", user=user, len = len(venues))
        return HTMLResponse(content=rendered_html)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        raise HTTPException(status_code=500, detail=error_message)
    


@app.get("/api/discover", response_class=JSONResponse)
async def api_discover(query: str = None, filters: str = None):
    try:
        venues = fetch_venues(query, filters)
        venues_list = [dict(venue) for venue in venues]
        return JSONResponse(content={"venues": venues_list})
    except Exception as e:
        error_message = f"An error occurred: {e}"
        return JSONResponse(content={"error": error_message}, status_code=500)

def fetch_venues(query: str, filters: str):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        sql_query = "SELECT * FROM venues"
        parameters = []

        if query:
            sql_query += """
                WHERE (
                    name LIKE ? OR
                    address LIKE ? OR
                    playground LIKE ? OR
                    fenced LIKE ? OR
                    quiet_zones LIKE ? OR
                    colors LIKE ? OR
                    smells LIKE ? OR
                    food_own LIKE ? OR
                    defined_duration LIKE ? OR
                    photo_url LIKE ? OR 
                    food_variey LIKE ?
                )
            """
            parameters.extend([f"%{query}%"] * 11)
        
        if filters:
            filters_dict = json.loads(filters)
            filter_clauses = []
            for key, value in filters_dict.items():
                if key == 'smells' or key == 'colors':
                    filter_clauses.append(f"{key} <= ?")
                    parameters.append(2)  # Restrict to values <= 2 for smells and colors
                
                elif key == 'food_variey':
                    filter_clauses.append(f"{key} >= ?")
                    parameters.append(3)  # Restrict to values >= 3 for food_variey

                elif key == 'defined_duration':
                    if value == 'NO':
                        filter_clauses.append(f"{key} = ?")
                        parameters.append(value)

                elif key in ['quiet_zones', 'playground', 'fenced', 'food_own']:
                    filter_clauses.append(f"{key} = ?")
                    parameters.append(value)

            if filter_clauses:
                if "WHERE" in sql_query:
                    sql_query += " AND " + " AND ".join(filter_clauses)
                else:
                    sql_query += " WHERE " + " AND ".join(filter_clauses)

        cursor.execute(sql_query, parameters)
        venues = cursor.fetchall()
        conn.close()
        return venues

    except sqlite3.Error as e:
        raise Exception(f"SQLite error: {e}")

    except json.JSONDecodeError as e:
        raise Exception(f"JSON decoding error: {e}")

    except Exception as e:
        raise Exception(f"An error occurred: {e}")


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
    template_path = app_path / "discover.html"
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
        food_variey: str = None
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
        "food_variey": food_variey
    }

    # Start with the base query
    query = "SELECT * FROM venues"
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

        # Load the discover.html template and render it with the filtered results
        template_path = app_path / "discover.html"
        with open(template_path, "r") as file:
            template = Template(file.read())

        rendered_html = template.render(venues=venues, filters=filters)
        return HTMLResponse(content=rendered_html)

    except Exception as e:
        logger.error(f"Error filtering venues: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)


@app.get("/venue/{venue_id}", response_class=HTMLResponse)
async def get_venue(venue_id: int, request: Request):
    """
    Retrieve and display details for a specific venue based on its ID, including reviews.
    """
    try:
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row  # Access columns by name
            cursor = conn.cursor()
            
            # Fetch venue details
            cursor.execute("SELECT * FROM venues WHERE id = ?", (venue_id,))
            venue = cursor.fetchone()  # Fetch the venue details

            if venue is None:
                return HTMLResponse(content="Venue not found", status_code=404)

            # Fetch reviews for the venue
            cursor.execute("SELECT * FROM reviews WHERE venue_id = ?", (venue_id,))
            reviews = cursor.fetchall()  # Fetch all reviews for the venue

        # Convert the sqlite3.Row objects to dictionaries for easier handling in the template
        venue_dict = dict(venue)
        reviews_dicts = [dict(review) for review in reviews]

        # Render the template with venue details and reviews
        template_path = app_path / "venue_page.html"
        with open(template_path, "r") as file:
            template = Template(file.read())
            user = request.cookies.get("user")
        rendered_html = template.render(venue=venue_dict, reviews=reviews_dicts, venue_id=venue_id, user=user)
        return HTMLResponse(content=rendered_html)

    except Exception as e:
        return HTMLResponse(content=f"An unexpected error occurred: {e}", status_code=500)



""" # Function to extract venue ID from the link (if needed elsewhere)
def extract_venue_id(link: str) -> int:
    match = re.search(r'/venue/(\d+)', link)
    if match:
        return int(match.group(1))
    raise ValueError("Invalid venue link. Could not extract venue ID.") """


@app.post("/register/")
async def register_user(nickname: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            cursor = conn.cursor()

            # Check if the nickname already exists
            cursor.execute("SELECT * FROM users WHERE nickname = ? OR email = ?", (nickname, email))
            existing_user = cursor.fetchone()

            if existing_user:
                if existing_user[1] == nickname:
                    logger.info(f"Username {nickname} already taken.")
                    return HTMLResponse(content="Username already taken", status_code=400)
                if existing_user[2] == email:
                    logger.info(f"Email {email} already taken.")
                    return HTMLResponse(content="Email already taken", status_code=400)

            # Hash the password for security
            hashed_password = bcrypt.hash(password)

            # Insert the new user into the database
            cursor.execute("INSERT INTO users (nickname, email, password) VALUES (?, ?, ?)", (nickname, email, hashed_password))
            conn.commit()

            logger.info(f"User {nickname} registered successfully.")
            # Redirect to the login page after successful registration
            return RedirectResponse(url="/login", status_code=303)

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
            if user and bcrypt.verify(password, user["password"]):
                response = RedirectResponse(url="/welcome", status_code=303)
                response.set_cookie(key="user", value=nickname)
                return response

            if not user:
                logger.info(f"Invalid login attempt for nickname {nickname}.")
                return HTMLResponse(content="Invalid nickname or password", status_code=400)

            # Verify the password
            if not bcrypt.verify(password, user["password"]):
                logger.info(f"Invalid password for nickname {nickname}.")
                return HTMLResponse(content="Invalid nickname or password", status_code=400)

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
        nickname = request.cookies.get("user")
        if not nickname:
            return HTMLResponse(content="Nickname not found in the request", status_code=400)

        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Fetch all reviews to display on the welcome page
            '''cursor.execute("""
                SELECT reviews.review_text, reviews.timestamp, users.nickname, venues.name AS venue_name
                FROM reviews
                JOIN users ON reviews.user_id = users.id
                JOIN venues ON reviews.venue_id = venues.id
                ORDER BY reviews.timestamp DESC
            """)'''
            reviews = cursor.fetchall()

            # Fetch all venues to populate the dropdown
            cursor.execute("SELECT id, name FROM venues")
            venues = cursor.fetchall()

        # Load dashboard.html template and render it with the reviews and venues data
        template_path = app_path / "dashboard.html"
        with open(template_path, "r") as file:
            template = Template(file.read())
        user = request.cookies.get("user")
        rendered_html = template.render(reviews=reviews, venues=venues, nickname=nickname, user=user)
        return HTMLResponse(content=rendered_html)

    except Exception as e:
        logger.error(f"Error loading welcome page: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("user")
    return response

@app.get("/aboutus", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.cookies.get("user")
    content = render_template(app_path / "aboutus.html", user=user)
    return HTMLResponse(content=content)


@app.get("/contactus", response_class=HTMLResponse)
async def read_root(request: Request):
    user = request.cookies.get("user")
    content = render_template(app_path / "contactus.html", user=user)
    return HTMLResponse(content=content)

@app.post("/request-venue/", response_class=HTMLResponse)
async def request_venue(
    request: Request,
    new_venue_name: str = Form(...),
    google_link: str = Form(None),
    colors: int = Form(None),
    smells: int = Form(None),
    quiet: int = Form(None),
    crowdedness: int = Form(None),
    food_variey: int = Form(None),
    playground: str = Form(None),
    fenced: str = Form(None),
    quiet_zones: str = Form(None),
    food_own: str = Form(None),
    defined_duration: str = Form(None)
):
    # Prepare SQL query to insert a new request into the database
    sql_query = """
        INSERT INTO requests (
            new_venue_name, google_link, colors, smells, quiet,
            crowdedness, food_variey, playground, fenced,
            quiet_zones, food_own, defined_duration
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    parameters = (
        new_venue_name, google_link, colors, smells, quiet,
        crowdedness, food_variey, playground, fenced,
        quiet_zones, food_own, defined_duration
    )

    # Connect to the database and execute the query
    with connect(db_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query, parameters)
        conn.commit()

    # Load the template to render a response
    template_path = app_path / "request_a_new_venue.html"  # Ensure this template exists
    with open(template_path, "r") as file:
        template = Template(file.read())

    rendered_html = template.render(message="Venue request submitted successfully!")
    return HTMLResponse(content=rendered_html)

@app.post("/login-admin/")
async def login_admin(username: str = Form(...), password: str = Form(...)):
    try:
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Check if the nickname exists
            cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and bcrypt.verify(password, user["password"]):
                response = RedirectResponse(url="/admin-dashboard", status_code=303)
                response.set_cookie(key="admin", value=username)
                return response

            if not user:
                logger.info(f"Invalid login attempt for nickname {username}.")
                return HTMLResponse(content="Invalid nickname or password", status_code=400)

            # Verify the password
            if not bcrypt.verify(password, user["password"]):
                logger.info(f"Invalid password for nickname {username}.")
                return HTMLResponse(content="Invalid nickname or password", status_code=400)

    except Exception as e:
        logger.error(f"Login error: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)
    
@app.get("/admin-dashboard", response_class=HTMLResponse)
async def get_admin_dashboard(request: Request, user_query: str = ""):
    try:
        admin = request.cookies.get("admin")
        if not admin:
            return HTMLResponse(content="Nickname not found in the request", status_code=400)

        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Fetch new venue requests
            cursor.execute("SELECT * FROM requests")
            new_requests = cursor.fetchall()

            # SQL query for searching users
            if user_query:
                user_sql_query = """
                    SELECT * FROM users WHERE
                    nickname LIKE ? OR
                    email LIKE ?
                """
                user_parameters = [f"%{user_query}%"] * 2  # Apply the search term to all fields
            else:
                user_sql_query = "SELECT * FROM users"
                user_parameters = []  # No parameters needed for a full table query

            cursor.execute(user_sql_query, user_parameters)
            users = cursor.fetchall()

            # Fetch all venues
            cursor.execute("SELECT * FROM venues")
            venues = cursor.fetchall()

    except Exception as e:
        logger.error(f"Error loading admin page: {e}")
        return HTMLResponse(content=f"An error occurred: {e}", status_code=500)

    try:
        template_path = app_path / "admin-dashboard.html"
        with open(template_path, "r") as file:
            template = Template(file.read())
            content = template.render(
                new_requests=new_requests,
                users=users,
                venues=venues,
                user=admin,
                search_query=user_query  # Pass the search query back to the template for displaying
            )
        return HTMLResponse(content=content)

    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        return HTMLResponse(content=f"An error occurred while rendering the page: {e}", status_code=500)

@app.post("/update-user")
async def update_user(
    user_id: int = Form(...),
    new_nickname: str = Form(""),
    new_email: str = Form("")
):
    try:
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            cursor = conn.cursor()

            # Update user information based on the provided new values
            if new_nickname:
                cursor.execute("UPDATE users SET nickname = ? WHERE id = ?", (new_nickname, user_id))
            if new_email:
                cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

            conn.commit()
            logger.info(f"Updated user {user_id} with new nickname '{new_nickname}' and new email '{new_email}'")

        return RedirectResponse(url="/admin-dashboard", status_code=302)

    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return HTMLResponse(content=f"An error occurred while updating the user: {e}", status_code=500)

@app.get("/admin-login", response_class=HTMLResponse)
async def get_admin_login():
    """
    Serves the admin-login.html file for admin login.
    """
    return FileResponse(app_path / "admin-login.html")


@app.get("/add-venue")

# We need to alter the query according to our "venues" table; also we need to alter the corresponding javascript.
# so far, the method add_venue is out of order
async def add_venue(name: str = Query(...)):
    try:
        # Here you can add the venue to the database with the provided name
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            cursor = conn.cursor()

            # Perform the insertion of the new venue
            cursor.execute("INSERT INTO venues (name) VALUES (?)", (name,))
            conn.commit()

            logger.info(f"Added new venue: {name}")

        return RedirectResponse(url="/admin-dashboard", status_code=302)

    except Exception as e:
        logger.error(f"Error adding venue: {e}")
        return HTMLResponse(content=f"An error occurred while adding the venue: {e}", status_code=500)

# Serve the entire app directory as static files
app.mount("/static", StaticFiles(directory=app_path, html=True), name="static")
