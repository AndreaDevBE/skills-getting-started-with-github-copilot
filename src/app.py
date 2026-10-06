"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice teamwork, drills, and match play on the field",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Basketball Club": {
        "description": "Develop shooting, passing, and defensive skills in a competitive setting",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Explore acting, stage performance, and dramatic storytelling",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Art Workshop": {
        "description": "Create paintings, sketches, and mixed-media projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": []
    },
    "Math Olympiad": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 10,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore STEM concepts through hands-on projects",
        "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    }
}


def normalize_email(email: str) -> str:
    return email.strip().lower()


def get_participant_emails(activity: dict) -> set[str]:
    return {normalize_email(participant) for participant in activity["participants"]}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/about-the-app")
def about_page():
    return FileResponse(current_dir / "static" / "about.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the activity
    activity = activities[activity_name]
    normalized_email = normalize_email(email)

    # Validate student is not already signed up
    if normalized_email in get_participant_emails(activity):
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up for this activity",
        )

    # Validate activity has capacity remaining
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = normalize_email(email)
    if normalized_email not in get_participant_emails(activity):
        raise HTTPException(
            status_code=404,
            detail="Student is not signed up for this activity",
        )

    activity["participants"] = [
        participant
        for participant in activity["participants"]
        if normalize_email(participant) != normalized_email
    ]
    return {"message": f"Unregistered {normalized_email} from {activity_name}"}
