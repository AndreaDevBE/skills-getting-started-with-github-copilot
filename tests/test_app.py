from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


INITIAL_ACTIVITIES = deepcopy(app_module.activities)
client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities(monkeypatch):
    monkeypatch.setattr(app_module, "activities", deepcopy(INITIAL_ACTIVITIES))


def test_get_activities_returns_all_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == INITIAL_ACTIVITIES


def test_signup_adds_participant():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up new.student@mergington.edu for Chess Club"
    }
    assert "new.student@mergington.edu" in client.get("/activities").json()[
        "Chess Club"
    ]["participants"]


def test_signup_rejects_existing_participant():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }


def test_signup_returns_404_for_unknown_activity():
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant():
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }
    assert "michael@mergington.edu" not in client.get("/activities").json()[
        "Chess Club"
    ]["participants"]


def test_unregister_returns_404_for_missing_participant():
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }


def test_unregister_returns_404_for_unknown_activity():
    response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}