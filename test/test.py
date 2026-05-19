import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

# Helper functions 
def register_user(
    client,
    email="test@example.com",
    name="Test User",
    password="password123",
    age=20
):
    return client.post("/register", json={
        "email": email,
        "name": name,
        "password": password,
        "age": age
    })


def login_user(client, email="test@example.com", password="password123"):
    return client.post("/login", json={
        "email": email,
        "password": password
    })

# Tests
def test_register_user_success(client):
    response = register_user(client)

    assert response.status_code in [200, 201]

    data = response.get_json()
    assert "id" in data
    assert data["id"] is not None


def test_register_missing_email(client):
    response = client.post("/register", json={
        "name": "No Email",
        "password": "password123",
        "age": 20
    })

    assert response.status_code in [400, 422]


def test_register_missing_password(client):
    response = client.post("/register", json={
        "email": "nopassword@example.com",
        "name": "No Password",
        "age": 20
    })

    assert response.status_code in [400, 422]


def test_login_success(client):
    register_response = register_user(
        client,
        email="login@example.com",
        name="Login User",
        password="password123",
        age=21
    )

    login_response = login_user(
        client,
        email="login@example.com",
        password="password123"
    )

    assert login_response.status_code == 200

    data = login_response.get_json()
    assert "id" in data
    assert data["id"] is register_response.get_json()["id"]


def test_login_wrong_password(client):
    register_user(
        client,
        email="wrongpass@example.com",
        name="Wrong Pass",
        password="correctpassword",
        age=22
    )

    response = login_user(
        client,
        email="wrongpass@example.com",
        password="wrongpassword"
    )

    assert response.status_code in [401, 403]


def test_login_nonexistent_user(client):
    response = login_user(
        client,
        email="doesnotexist@example.com",
        password="password123"
    )

    assert response.status_code in [401, 404]


def test_get_user_info_success(client):
    register_response = register_user(
        client,
        email="profile@example.com",
        name="Profile User",
        password="password123",
        age=25
    )

    user_id = register_response.get_json()["id"]

    response = client.get(f"/{user_id}")

    assert response.status_code == 200

    data = response.get_json()
    assert data["email"] == "profile@example.com"
    assert data["name"] == "Profile User"
    assert data["age"] == 25


def test_get_user_info_invalid_id(client):
    response = client.get("/999999")

    assert response.status_code in [400, 404]


def test_search_gyms_success(client):
    register_response = register_user(
        client,
        email="search@example.com",
        name="Search User",
        password="password123",
        age=23
    )

    user_id = register_response.get_json()["id"]

    response = client.get(f"/{user_id}/search", query_string={
        "longitude": 151.2093,
        "latitude": -33.8688,
        "limit": 10,
        "radius_km": 5
    })

    assert response.status_code == 200

    data = response.get_json()
    assert "gyms" in data
    assert isinstance(data["gyms"], list)
    assert len(data["gyms"]) > 0


def test_search_gyms_missing_longitude(client):
    register_response = register_user(
        client,
        email="missinglongitude@example.com",
        name="Missing Longitude",
        password="password123",
        age=24
    )

    user_id = register_response.get_json()["id"]

    response = client.get(f"/{user_id}/search", query_string={
        "latitude": -33.8688,
        "limit": 10,
        "radius_km": 5
    })

    assert response.status_code in [400, 422]


def test_search_gyms_missing_latitude(client):
    register_response = register_user(
        client,
        email="missinglatitude@example.com",
        name="Missing Latitude",
        password="password123",
        age=24
    )

    user_id = register_response.get_json()["id"]

    response = client.get(f"/{user_id}/search", query_string={
        "longitude": 151.2093,
        "limit": 10,
        "radius_km": 5
    })

    assert response.status_code in [400, 422]


def test_search_groups_success(client):
    register_response = register_user(
        client,
        email="groupssearch@example.com",
        name="Groups Search User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    response = client.get(f"/{user_id}/groups", query_string={
        "gym_name": "Anytime Fitness",
        "time_start": "2026-06-01T18:00:00",
        "time_end": "2026-06-01T19:00:00"
    })

    assert response.status_code == 200

    data = response.get_json()
    assert "groups" in data
    assert isinstance(data["groups"], list)


def test_search_groups_missing_gym_name(client):
    register_response = register_user(
        client,
        email="missinggymname@example.com",
        name="Missing Gym Name",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    response = client.get(f"/{user_id}/groups", query_string={
        "time_start": "2026-06-01T18:00:00",
        "time_end": "2026-06-01T19:00:00"
    })

    assert response.status_code in [400, 422]


def test_create_group_success(client):
    register_response = register_user(
        client,
        email="creategroup@example.com",
        name="Create Group User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    response = client.post(f"/{user_id}/groups", json={
        "gym": "Anytime Fitness",
        "time_start": "2026-06-01T18:00:00",
        "time_end": "2026-06-01T19:00:00",
        "members": [user_id]
    })

    assert response.status_code in [200, 201]

    data = response.get_json()
    assert "id" in data
    assert data["id"] is not None


def test_create_group_missing_gym(client):
    register_response = register_user(
        client,
        email="nogym@example.com",
        name="No Gym User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    response = client.post(f"/{user_id}/groups", json={
        "time_start": "2026-06-01T18:00:00",
        "time_end": "2026-06-01T19:00:00",
        "members": [user_id]
    })

    assert response.status_code in [400, 422]


def test_create_group_missing_time_start(client):
    register_response = register_user(
        client,
        email="notimestart@example.com",
        name="No Time Start User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    response = client.post(f"/{user_id}/groups", json={
        "gym": "Anytime Fitness",
        "time_end": "2026-06-01T19:00:00",
        "members": [user_id]
    })

    assert response.status_code in [400, 422]


def test_join_group_success(client):
    register_response = register_user(
        client,
        email="joiner@example.com",
        name="Join Group User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_group_response = client.post(f"/{user_id}/groups", json={
        "gym": "Anytime Fitness",
        "time_start": "2026-06-01T18:00:00",
        "time_end": "2026-06-01T19:00:00",
        "members": []
    })

    group_id = create_group_response.get_json()["id"]

    response = client.put(f"/{user_id}/groups/{group_id}", json={
        "id": user_id,
        "group_id": group_id
    })

    assert response.status_code in [200, 204]


def test_join_group_invalid_group_id(client):
    register_response = register_user(
        client,
        email="badjoin@example.com",
        name="Bad Join User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    response = client.put(f"/{user_id}/groups/999999", json={
        "id": user_id,
        "group_id": 999999
    })

    assert response.status_code in [400, 404]


def test_leave_group_success(client):
    register_response = register_user(
        client,
        email="leaver@example.com",
        name="Leave Group User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_group_response = client.post(f"/{user_id}/groups", json={
        "gym": "Anytime Fitness",
        "time_start": "2026-06-01T18:00:00",
        "time_end": "2026-06-01T19:00:00",
        "members": [user_id]
    })

    group_id = create_group_response.get_json()["id"]

    response = client.put(f"/{user_id}/groups/{group_id}/leave")

    assert response.status_code in [200, 204]


def test_leave_group_invalid_group_id(client):
    register_response = register_user(
        client,
        email="badleave@example.com",
        name="Bad Leave User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    response = client.put(f"/{user_id}/groups/999999/leave")

    assert response.status_code in [400, 404]


def test_delete_group_success(client):
    register_response = register_user(
        client,
        email="deletegroup@example.com",
        name="Delete Group User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_group_response = client.post(f"/{user_id}/groups", json={
        "gym": "Anytime Fitness",
        "time_start": "2026-06-01T18:00:00",
        "time_end": "2026-06-01T19:00:00",
        "members": [user_id]
    })

    group_id = create_group_response.get_json()["id"]

    response = client.delete(f"/{user_id}/groups/{group_id}")

    assert response.status_code in [200, 204]


def test_delete_group_invalid_group_id(client):
    register_response = register_user(
        client,
        email="baddelete@example.com",
        name="Bad Delete User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    response = client.delete(f"/{user_id}/groups/999999")

    assert response.status_code in [400, 404]