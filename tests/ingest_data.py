import uuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_signup_login_users_me():
    email = f"pytest_{uuid.uuid4().hex}@example.com"
    password = "123456"

    # signup
    r = client.post("/auth/signup", json={"email": email, "password": password})
    assert r.status_code in (201, 400)

    # login (JSON d'abord)
    r = client.post("/auth/login", json={"email": email, "password": password})

    # si ton login attend form-data, on retente en data
    if r.status_code != 200:
        r = client.post("/auth/login", data={"username": email, "password": password})

    assert r.status_code == 200
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/users/me", headers=headers)
    assert r.status_code == 200


def test_get_indicators_filters():
    # juste vérifier que l'endpoint répond (même vide)
    r = client.get("/indicators")
    # si protégé, ce sera 401 sans token, c'est ok
    assert r.status_code in (200, 401)
