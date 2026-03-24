from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange - TestClient is initialized with the app

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Verify structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club


def test_signup_success():
    # Arrange
    activity = "Basketball Team"
    email = "newplayer@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert f"Signed up {email} for {activity}" == response_data["message"]


def test_signup_activity_not_found():
    # Arrange
    activity = "NonExistent Activity"
    email = "test@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    response_data = response.json()
    assert "detail" in response_data
    assert "Activity not found" == response_data["detail"]


def test_signup_already_signed_up():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    response_data = response.json()
    assert "detail" in response_data
    assert "Student is already signed up for this activity" == response_data["detail"]