# test_main.py
import sqlite3
import pytest
from fastapi.testclient import TestClient
from main import app  # Import the FastAPI app from main.py
import bcrypt

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
        defined_duration TEXT
    );
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT UNIQUE,
        password TEXT
    );
    """)
    conn.commit()
    conn.close()

    # Monkey-patch the db_path in the main app to point to this temporary database
    app.dependency_overrides[lambda: db_path] = lambda: db_file

    yield db_file  # Provide the test DB to the test functions

    # Cleanup the database file after tests
    db_file.unlink()


def test_get_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_signup():
    response = client.get("/signup")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@pytest.mark.asyncio
async def test_search_venues(setup_test_db):
    response = client.get("/search-venues/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    response = client.get("/search-venues/?query=test")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@pytest.mark.asyncio
async def test_filter_venues(setup_test_db):
    response = client.get("/filter-venues/?name=test&address=test")
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

  #  @pytest.mark.asyncio
  #  async def test_register_user(client, setup_test_db):
  #      # Arrange
  #      nickname = "test"
  #      password = "test"
  #      hashed_password = bcrypt.hash(password)

        # Act
  #      response = client.post("/register/", data={"nickname": nickname, "password": password})

        # Assert
  #      assert response.status_code == 303
  #      assert response.headers["location"] == "/static/login.html"
  #      test_db.execute("SELECT * FROM users WHERE nickname = ?", (nickname,))
  #      user = test_db.fetchone()
  #      assert user is not None
  #      assert user[0] == nickname
  #      assert bcrypt.verify(password, user[1])
    
#@pytest.mark.asyncio
#async def test_login_user(setup_test_db):
#    # Register a user first
#    client.post("/register/", data={"nickname": "testuser", "password": "testpass"})

    # Login with the registered user
#    response = client.post("/login/", data={"nickname": "testuser", "password": "testpass"})
#    assert response.status_code == 200  # Expect a redirect

    # Attempt to login with invalid credentials
#    response = client.post("/login/", data={"nickname": "testuser", "password": "wrongpass"})
#    assert response.status_code == 400  # Invalid credentials

#def test_get_welcome():
 #   response = client.get("/welcome")
  #  assert response.status_code == 200
   # assert "text/html" in response.headers["content-type"]
