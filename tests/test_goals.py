import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

import pytest
from fastapi.testclient import TestClient
from datetime import date

def test_create_goal(client: TestClient):
    response = client.post("/api/goals", json={
        "name": "Vacation Fund",
        "target_minor": 500000,
        "current_minor": 100000,
        "target_date": "2027-12-31",
        "currency": "USD"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Vacation Fund"
    assert data["target_minor"] == 500000
    assert data["progress"] == 0.2

def test_get_goals(client: TestClient):
    # Ensure there's a goal
    client.post("/api/goals", json={
        "name": "Emergency Fund",
        "target_minor": 1000000,
        "current_minor": 250000,
        "currency": "USD"
    })
    
    response = client.get("/api/goals")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    
    goal = next(g for g in data["items"] if g["name"] == "Emergency Fund")
    assert goal["progress"] == 0.25
    assert goal["target_minor"] == 1000000


def test_delete_goal(client: TestClient):
    response = client.post("/api/goals", json={
        "name": "Trip Fund",
        "target_minor": 200000,
        "current_minor": 50000,
        "target_date": "2027-06-30",
        "currency": "USD"
    })
    goal_id = response.json()["id"]

    delete_response = client.delete(f"/api/goals/{goal_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["deleted"] is True
    assert delete_response.json()["id"] == goal_id

    list_response = client.get("/api/goals")
    assert list_response.status_code == 200
    assert all(item["id"] != goal_id for item in list_response.json()["items"])
