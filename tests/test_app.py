from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_and_unregister_flow():
    activity_name = "Chess Club"
    email = "pyteststudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

    unregister_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert unregister_response.status_code == 200

    activities_after = client.get("/activities").json()
    assert email not in activities_after[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    activity_name = "Programming Class"
    email = "duplicate@mergington.edu"

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second_response.status_code == 400
