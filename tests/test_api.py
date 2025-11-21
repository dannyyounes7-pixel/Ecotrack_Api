from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "Bienvenue" in r.json()["message"]

def test_signup_and_login():
    email = "test_user@example.com"
    password = "123456"

    # Signup
    r = client.post("/auth/signup", json={"email": email, "password": password})
    assert r.status_code in (201, 400)

    # Login
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    assert "access_token" in r.json()
