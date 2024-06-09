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

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Example query: Retrieve all records from the venues table
    cursor.execute("SELECT * FROM venues")
    venues = cursor.fetchall()

    # Print out the retrieved venues for debugging
    print("Retrieved venues:", venues)

    # Close the database connection
    conn.close()

except sqlite3.Error as e:
    # Handle any database errors
    print("Database error:", e)

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

# Serve the entire app directory as static files
app.mount("/static", StaticFiles(directory=app_path, html=True), name="static")