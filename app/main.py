import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
from pathlib import Path

app = FastAPI()

# Define the path to the app directory
app_path = Path(__file__).parent

# Serve the entire app directory as static files
app.mount("/static", StaticFiles(directory=app_path, html=True), name="static")

# Database connection to venues.db
db_path = app_path / 'venues.db'

@app.get("/", response_class=HTMLResponse)
def get_index():
    """
    Serves the index.html file at the root path.
    """
    return FileResponse(app_path / "index.html")

@app.get("/search-venues/", response_class=HTMLResponse)
async def search_venues(request: Request):
    """
    Handles the initial search and shows venues based on the general search term.
    If no query is provided, display all venues.
    """
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
            defined_duration LIKE ?
        """
        parameters = [f"%{query}%"] * 9  # Apply the search term to all fields
    else:
        sql_query = "SELECT * FROM venues"
        parameters = []  # No parameters needed for a full table query

    # Connect to the database and execute the query
    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query, parameters)
        venues = cursor.fetchall()

    # Load filter.html template and render it with the search results
    template_path = app_path / "filter.html"
    with open(template_path, "r") as file:
        template = Template(file.read())

    rendered_html = template.render(venues=venues, query=query)
    return HTMLResponse(content=rendered_html)

@app.get("/filter-venues/", response_class=HTMLResponse)
async def filter_venues(
    request: Request,
    name: str = "",
    address: str = "",
    playground: str = "",
    fenced: str = "",
    quiet_zones: str = "",
    colors: str = "",
    smells: str = "",
    food_own: str = "",
    defined_duration: str = "",
    quiet: str = "",
    crowdedness: str = "",
    food_variey: str = ""
):
    """
    Handles detailed filtering of venues based on user-selected criteria.
    If no filter options are provided, select all entries.
    """
    # Build the SQL query dynamically based on provided filtering parameters
    query = "SELECT * FROM venues WHERE 1=1"
    parameters = []

    if name:
        query += " AND name LIKE ?"
        parameters.append(f"%{name}%")
    if address:
        query += " AND address LIKE ?"
        parameters.append(f"%{address}%")
    if playground:
        query += " AND playground LIKE ?"
        parameters.append(f"%{playground}%")
    if fenced:
        query += " AND fenced LIKE ?"
        parameters.append(f"%{fenced}%")
    if quiet_zones:
        query += " AND quiet_zones LIKE ?"
        parameters.append(f"%{quiet_zones}%")
    if colors:
        query += " AND colors LIKE ?"
        parameters.append(f"%{colors}%")
    if smells:
        query += " AND smells LIKE ?"
        parameters.append(f"%{smells}%")
    if food_own:
        query += " AND food_own LIKE ?"
        parameters.append(f"%{food_own}%")
    if defined_duration:
        query += " AND defined_duration LIKE ?"
        parameters.append(f"%{defined_duration}%")
    if quiet:
        query += " AND quiet LIKE ?"
        parameters.append(f"%{quiet}%")
    if crowdedness:
        query += " AND crowdedness LIKE ?"
        parameters.append(f"%{crowdedness}%")
    if food_variey:
        query += " AND food_variey LIKE ?"
        parameters.append(f"%{food_variey}%")

    if not any([name, address, playground, fenced, quiet_zones, colors, smells, food_own, defined_duration, quiet, crowdedness, food_variey]):
        # If no filter options are provided, select all entries
        query = "SELECT * FROM venues"
        parameters = []

    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        venues = cursor.fetchall()

    # Load searchresults.html template and render it with the filtered search results
    template_path = app_path / "searchresults.html"
    with open(template_path, "r") as file:
        template = Template(file.read())

    rendered_html = template.render(venues=venues)
    return HTMLResponse(content=rendered_html)

@app.get("/venue/{venue_id}", response_class=HTMLResponse)
async def get_venue(venue_id: int):
    """
    Retrieve and display details for a specific venue based on its ID.
    """
    print("here")
    try:
        # Connect to the database
        with sqlite3.connect(db_path, check_same_thread=False) as conn:
            conn.row_factory = sqlite3.Row  # Access columns by name
            cursor = conn.cursor()
            print(f"Fetching venue with ID: {venue_id}")  # Debug log
            cursor.execute("SELECT * FROM venues WHERE id = ?", (venue_id,))
            venue = cursor.fetchone()  # Fetch the venue details
            print(f"Fetched venue: {venue}")  # Debug log

        if venue is None:
            print("Venue not found")  # Debug log
            return HTMLResponse(content="Venue not found", status_code=404)

        # Convert the sqlite3.Row object to a dictionary for easier handling in the template
        venue_dict = dict(venue)
    except Exception as e:
        # Log the error for debugging
        print(f"Error: {e}")
        return HTMLResponse(content=f"An unexpected error occurred {e}", status_code=491)
    try:
        # Debug log for venue details
        print(f"Venue details: {venue_dict}")

        # Load the venue_page.html template and render it with the venue's details
        template_path = app_path / "venue_page.html"
        print(f"Template path: {template_path}")  # Debug log
        with open(template_path, "r") as file:
            template = Template(file.read())

        rendered_html = template.render(venue=venue_dict)
        return HTMLResponse(content=rendered_html)

    except Exception as e:
        # Log the error for debugging
        print(f"Error: {e}")
        return HTMLResponse(content=f"{venue_dict}, {template_path}An unexpected error occurred {e}", status_code=490)
   # rendered_html = template.render(venue=venue)
   # return HTMLResponse(content=rendered_html)



# Serve the entire app directory as static files
app.mount("/static", StaticFiles(directory=app_path, html=True), name="static")