import sqlite3
import pytest
from fastapi.testclient import TestClient
from main import app  # Import the FastAPI app from main.py

# Initialize the TestClient with our FastAPI app
client = TestClient(app)

# A fixture to create a temporary SQLite database for testing
@pytest.fixture(scope="module")
def setup_test_db(tmp_path_factory):
    # Create a temporary database file
    db_file = tmp_path_factory.mktemp("data") / "test_venues.db"
    
    # Connect to the temporary database and set up the schema
    conn = sqlite3.connect(db_file, check_same_thread=False)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE venues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        playground TEXT,
        fenced TEXT,
        quiet_zones TEXT,
        colors TEXT,
        smells TEXT,
        food_own TEXT,
        defined_duration TEXT,
        photo_url TEXT
    );
    """)
    conn.commit()
    conn.close()

    # Monkey-patch the db_path in the main app to point to this temporary database
    app.dependency_overrides[lambda: db_path] = lambda: db_file

    yield db_file  # Provide the test DB to the test functions

    # Cleanup the database file after tests
    db_file.unlink()

def populate_test_db(db_file):
    """
    Populate the test database with sample data.
    """
    with sqlite3.connect(db_file, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.executemany("""
        INSERT INTO venues (name, address, playground, fenced, quiet_zones, colors, smells, food_own, defined_duration, photo_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [
            ("Venue A", "Address A", "Yes", "No", "Yes", "Bright", "Mild", "No", "1-2 hours", "/static/images/venueA.png"),
            ("Venue B", "Address B", "No", "Yes", "No", "Dark", "None", "Yes", "2-3 hours", "/static/images/venueB.png"),
            ("Venue C", "Address C", "Yes", "Yes", "Yes", "Colorful", "Strong", "No", "3-4 hours", "/static/images/venueC.png")
        ])
        conn.commit()

@pytest.mark.asyncio
async def test_search_venues_no_query(setup_test_db):
    populate_test_db(setup_test_db)

    response = client.get("/search-venues/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    # Ensure all venues are returned when no query is provided
    assert "Venue A" in response.text
    assert "Venue B" in response.text
    assert "Venue C" in response.text

@pytest.mark.asyncio
async def test_search_venues_with_query(setup_test_db):
    populate_test_db(setup_test_db)

    response = client.get("/search-venues/?query=Venue")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    # Ensure the response contains the expected results
    assert "Venue A" in response.text
    assert "Venue B" in response.text
    assert "Venue C" in response.text

    response = client.get("/search-venues/?query=Address B")
    assert response.status_code == 200
    assert "Venue B" in response.text
    assert "Venue A" not in response.text
    assert "Venue C" not in response.text

    response = client.get("/search-venues/?query=Colorful")
    assert response.status_code == 200
    assert "Venue C" in response.text
    assert "Venue A" not in response.text
    assert "Venue B" not in response.text

@pytest.mark.asyncio
async def test_search_venues_no_match(setup_test_db):
    populate_test_db(setup_test_db)

    response = client.get("/search-venues/?query=NonExistent")
    assert response.status_code == 200
    assert "No venues found matching your query." in response.text  # Assumes the template displays this message

def test_get_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_signup():
    response = client.get("/signup")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
@pytest.mark.asyncio
async def test_get_venue(setup_test_db):
    # Add a test venue
    with sqlite3.connect(setup_test_db, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO venues (name, address) VALUES (?, ?)", ("Test Venue", "Test Address"))
        venue_id = cursor.lastrowid
        conn.commit()

    response = client.get(f"/venue/{venue_id}")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    response = client.get("/venue/9999")  # Non-existent venue
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_login_user(setup_test_db):
    # Register a user first
    client.post("/register/", data={"nickname": "testuser", "password": "testpass"})

    # Login with the registered user
    response = client.post("/login/", data={"nickname": "testuser", "password": "testpass"})
    assert response.status_code == 200  # Expect a redirect

    # Attempt to login with invalid credentials
    response = client.post("/login/", data={"nickname": "testuser", "password": "wrongpass"})
    assert response.status_code == 400  # Invalid credentials

def test_get_welcome():
    response = client.get("/welcome")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
