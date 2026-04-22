from src.app import activities


def test_unregister_success_removes_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_fails_when_activity_not_found(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants", params={"email": "a@b.com"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_when_participant_not_registered(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "not.registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_signup_unregister_signup_flow_is_consistent(client):
    activity_name = "Drama Club"
    email = "flow.student@mergington.edu"

    first_signup = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    unregister = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )
    second_signup = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    assert first_signup.status_code == 200
    assert unregister.status_code == 200
    assert second_signup.status_code == 200
    assert activities[activity_name]["participants"].count(email) == 1
