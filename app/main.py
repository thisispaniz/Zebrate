import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template
from pathlib import Path

app = FastAPI()

# Define the path to the app directory
app_path = Path(__file__).parent

# Database connection to venue.db
conn = sqlite3.connect(app_path / 'venues.db', check_same_thread=False)
conn.row_factory = sqlite3.Row  # Allows accessing columns by name

@app.get("/", response_class=HTMLResponse)
def get_index():
    """
    Serves the index.html file at the root path.
    """
    return FileResponse(app_path / "index.html")

@app.get("/search-venues/", response_class=HTMLResponse)
async def search_venues(
    request: Request,
    query: str = ""
):
    """
    Handles the initial search and shows venues based on the general search term.
    """
    # Build the SQL query to search across multiple fields
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

    with sqlite3.connect(app_path / 'venue.db', check_same_thread=False) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query, parameters)
        venues = cursor.fetchall()

    # Load filter.html template and render it with the initial search results
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
    defined_duration: str = ""
):
    """
    Handles detailed filtering of venues based on user-selected criteria.
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

    with sqlite3.connect(app_path / 'venue.db', check_same_thread=False) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        venues = cursor.fetchall()

    # Load venue.html template and render it with the filtered search results
    template_path = app_path / "venue.html"
    with open(template_path, "r") as file:
        template = Template(file.read())

    rendered_html = template.render(venues=venues, query=request.query_params)
    return HTMLResponse(content=rendered_html)

# Serve the entire app directory as static files
app.mount("/", StaticFiles(directory=app_path, html=True), name="static")
