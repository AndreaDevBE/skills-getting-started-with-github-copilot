from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_student_cannot_sign_up_twice_for_same_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = list(activities[activity_name]["participants"])

    try:
        activities[activity_name]["participants"] = [email]
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 400
        assert response.json() == {"detail": "Student is already signed up"}
    finally:
        activities[activity_name]["participants"] = original_participants


def test_student_can_sign_up_when_not_already_registered():
    activity_name = "Chess Club"
    email = "freshstudent@mergington.edu"
    original_participants = list(activities[activity_name]["participants"])

    try:
        activities[activity_name]["participants"] = ["existing@mergington.edu"]
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
        assert email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants
