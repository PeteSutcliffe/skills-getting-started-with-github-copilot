from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)
original_activities = deepcopy(activities)


def reset_activity_data():
    activities.clear()
    activities.update(deepcopy(original_activities))


def setup_function():
    reset_activity_data()


def teardown_function():
    reset_activity_data()


def test_get_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == activities


def test_signup_for_activity():
    activity_name = "Chess Club"
    email = "test_student@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_participant():
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }


def test_unregister_participant():
    activity_name = "Programming Class"
    email = activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant():
    activity_name = "Soccer Team"
    email = "nonexistent@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Participant not found in this activity"
    }
