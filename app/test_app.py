import json
import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200

def test_index_increments_visits(client):
    r1 = client.get("/")
    r2 = client.get("/")
    assert r2.json["visits"] == r1.json["visits"] + 1

def test_reset_zeros_counter(client):
    client.get("/")
    response = client.post("/reset")
    assert response.json["visits"] == 0

def test_reset_requires_post(client):
    response = client.get("/reset")
    assert response.status_code == 405

def test_stats_returns_full_info(client):
    response = client.get("/stats")
    assert "hostname" in response.json
    assert "redis_host" in response.json
    assert "visits" in response.json
