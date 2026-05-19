import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

# -------------------------
# Helper functions
# -------------------------

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


def create_group(
    client,
    user_id,
    gym="Anytime Fitness",
    time_start="2026-06-01T18:00:00",
    time_end="2026-06-01T19:00:00",
    members=None
):
    if members is None:
        members = [user_id]

    return client.post(f"/{user_id}/groups", json={
        "gym": gym,
        "time_start": time_start,
        "time_end": time_end,
        "members": members
    })


def get_group_by_id(groups, group_id):
    for group in groups:
        if str(group["id"]) == str(group_id):
            return group
    return None

# -------------------------
# Tests
# -------------------------

# -------------------------
# Register / login
# -------------------------

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
    register_user(
        client,
        email="login@example.com",
        name="Login User",
        password="password123",
        age=21
    )

    response = login_user(
        client,
        email="login@example.com",
        password="password123"
    )

    assert response.status_code == 200

    data = response.get_json()
    assert "id" in data


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


# -------------------------
# User info
# -------------------------

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


def test_get_user_info_invalid_id(client):
    response = client.get("/999999")

    assert response.status_code in [400, 404]


# -------------------------
# Gym search
# -------------------------

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
        "longitude": -0.1276,
        "latitude": 51.5072,
        "limit": 10,
        "radius_km": 10
    })

    assert response.status_code == 200

    data = response.get_json()

    assert "gyms" in data
    assert isinstance(data["gyms"], list)
    assert len(data["gyms"]) > 0

    for gym in data["gyms"]:
        assert isinstance(gym, str)
        assert len(gym) > 0
        

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


# -------------------------
# Create groups
# -------------------------

def test_create_group_success(client):
    register_response = register_user(
        client,
        email="creategroup@example.com",
        name="Create Group User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    response = create_group(
        client,
        user_id=user_id,
        gym="Anytime Fitness",
        members=[user_id]
    )

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


# -------------------------
# Search groups by user
# -------------------------

def test_search_groups_finds_created_group(client):
    register_response = register_user(
        client,
        email="searchgroups@example.com",
        name="Search Groups User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_response = create_group(
        client,
        user_id=user_id,
        gym="Anytime Fitness",
        time_start="2026-06-01T18:00:00",
        time_end="2026-06-01T19:00:00",
        members=[user_id]
    )

    group_id = create_response.get_json()["id"]

    response = client.get(f"/{user_id}/groups", query_string={
        "gym_name": "Anytime Fitness",
        "time_start": "2026-06-01T17:00:00",
        "time_end": "2026-06-01T20:00:00"
    })

    assert response.status_code == 200

    data = response.get_json()
    assert "groups" in data

    group = get_group_by_id(data["groups"], group_id)

    assert group is not None
    assert group["gym"] == "Anytime Fitness"
    assert group["time_start"] == "2026-06-01T18:00:00"
    assert group["time_end"] == "2026-06-01T19:00:00"

    member_names = [member["name"] for member in group["members"]]
    assert "Search Groups User" in member_names


def test_search_groups_does_not_return_wrong_gym(client):
    register_response = register_user(
        client,
        email="wronggymsearch@example.com",
        name="Wrong Gym Search User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_group(
        client,
        user_id=user_id,
        gym="Fitness First",
        members=[user_id]
    )

    response = client.get(f"/{user_id}/groups", query_string={
        "gym_name": "Anytime Fitness",
        "time_start": "2026-06-01T17:00:00",
        "time_end": "2026-06-01T20:00:00"
    })

    assert response.status_code == 200

    data = response.get_json()
    assert data["groups"] == []


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
        "time_start": "2026-06-01T17:00:00",
        "time_end": "2026-06-01T20:00:00"
    })

    assert response.status_code in [400, 422]


# -------------------------
# Get current groups
# -------------------------

def test_get_current_groups_contains_joined_group(client):
    register_response = register_user(
        client,
        email="currentgroups@example.com",
        name="Current Groups User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_response = create_group(
        client,
        user_id=user_id,
        gym="Anytime Fitness",
        members=[user_id]
    )

    group_id = create_response.get_json()["id"]

    response = client.get(f"/{user_id}/groups/current")

    assert response.status_code == 200

    data = response.get_json()
    assert "groups" in data

    group = get_group_by_id(data["groups"], group_id)

    assert group is not None
    assert group["gym"] == "Anytime Fitness"

    member_names = [member["name"] for member in group["members"]]
    assert "Current Groups User" in member_names


def test_get_current_groups_empty_after_leaving(client):
    register_response = register_user(
        client,
        email="emptycurrent@example.com",
        name="Empty Current User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_response = create_group(
        client,
        user_id=user_id,
        gym="Anytime Fitness",
        members=[user_id]
    )

    group_id = create_response.get_json()["id"]

    client.put(f"/{user_id}/groups/{group_id}/leave")

    response = client.get(f"/{user_id}/groups/current")

    assert response.status_code == 200

    data = response.get_json()
    assert data["groups"] == []


# -------------------------
# Get groups by gym
# -------------------------

def test_get_gym_groups_contains_created_group(client):
    register_response = register_user(
        client,
        email="gymgroups@example.com",
        name="Gym Groups User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_response = create_group(
        client,
        user_id=user_id,
        gym="Anytime Fitness",
        members=[user_id]
    )

    group_id = create_response.get_json()["id"]

    response = client.get("/groups/Anytime Fitness")

    assert response.status_code == 200

    data = response.get_json()
    assert "groups" in data

    group = get_group_by_id(data["groups"], group_id)

    assert group is not None
    assert group["gym"] == "Anytime Fitness"

    member_names = [member["name"] for member in group["members"]]
    assert "Gym Groups User" in member_names


def test_get_gym_groups_does_not_return_other_gyms(client):
    register_response = register_user(
        client,
        email="othergymgroups@example.com",
        name="Other Gym Groups User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_group(
        client,
        user_id=user_id,
        gym="Fitness First",
        members=[user_id]
    )

    response = client.get("/groups/Anytime Fitness")

    assert response.status_code == 200

    data = response.get_json()
    assert data["groups"] == []


# -------------------------
# Join group
# -------------------------

def test_join_group_modifies_members(client):
    owner_response = register_user(
        client,
        email="owner@example.com",
        name="Owner User",
        password="password123",
        age=21
    )

    joiner_response = register_user(
        client,
        email="joiner@example.com",
        name="Joiner User",
        password="password123",
        age=22
    )

    owner_id = owner_response.get_json()["id"]
    joiner_id = joiner_response.get_json()["id"]

    create_response = create_group(
        client,
        user_id=owner_id,
        gym="Anytime Fitness",
        members=[owner_id]
    )

    group_id = create_response.get_json()["id"]

    join_response = client.put(f"/{joiner_id}/groups/{group_id}", json={
        "id": joiner_id,
        "group_id": group_id
    })

    assert join_response.status_code in [200, 204]

    current_response = client.get(f"/{joiner_id}/groups/current")

    assert current_response.status_code == 200

    data = current_response.get_json()
    group = get_group_by_id(data["groups"], group_id)

    assert group is not None

    member_names = [member["name"] for member in group["members"]]
    assert "Owner User" in member_names
    assert "Joiner User" in member_names


def test_join_group_twice_does_not_duplicate_member(client):
    owner_response = register_user(
        client,
        email="owner2@example.com",
        name="Owner Two",
        password="password123",
        age=21
    )

    joiner_response = register_user(
        client,
        email="joiner2@example.com",
        name="Joiner Two",
        password="password123",
        age=22
    )

    owner_id = owner_response.get_json()["id"]
    joiner_id = joiner_response.get_json()["id"]

    create_response = create_group(
        client,
        user_id=owner_id,
        gym="Anytime Fitness",
        members=[owner_id]
    )

    group_id = create_response.get_json()["id"]

    client.put(f"/{joiner_id}/groups/{group_id}", json={
        "id": joiner_id,
        "group_id": group_id
    })

    client.put(f"/{joiner_id}/groups/{group_id}", json={
        "id": joiner_id,
        "group_id": group_id
    })

    response = client.get(f"/{joiner_id}/groups/current")

    data = response.get_json()
    group = get_group_by_id(data["groups"], group_id)

    member_names = [member["name"] for member in group["members"]]

    assert member_names.count("Joiner Two") == 1


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


# -------------------------
# Leave group
# -------------------------

def test_leave_group_modifies_members(client):
    register_response = register_user(
        client,
        email="leaver@example.com",
        name="Leave Group User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_response = create_group(
        client,
        user_id=user_id,
        gym="Anytime Fitness",
        members=[user_id]
    )

    group_id = create_response.get_json()["id"]

    leave_response = client.put(f"/{user_id}/groups/{group_id}/leave")

    assert leave_response.status_code in [200, 204]

    current_response = client.get(f"/{user_id}/groups/current")

    data = current_response.get_json()
    group = get_group_by_id(data["groups"], group_id)

    assert group is None


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


# -------------------------
# Delete group
# -------------------------

def test_delete_group_removes_group_from_user_search(client):
    register_response = register_user(
        client,
        email="deletegroup@example.com",
        name="Delete Group User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_response = create_group(
        client,
        user_id=user_id,
        gym="Anytime Fitness",
        members=[user_id]
    )

    group_id = create_response.get_json()["id"]

    delete_response = client.delete(f"/{user_id}/groups/{group_id}")

    assert delete_response.status_code in [200, 204]

    search_response = client.get(f"/{user_id}/groups", query_string={
        "gym_name": "Anytime Fitness",
        "time_start": "2026-06-01T17:00:00",
        "time_end": "2026-06-01T20:00:00"
    })

    data = search_response.get_json()
    group = get_group_by_id(data["groups"], group_id)

    assert group is None


def test_delete_group_removes_group_from_gym_groups(client):
    register_response = register_user(
        client,
        email="deletegymgroup@example.com",
        name="Delete Gym Group User",
        password="password123",
        age=20
    )

    user_id = register_response.get_json()["id"]

    create_response = create_group(
        client,
        user_id=user_id,
        gym="Anytime Fitness",
        members=[user_id]
    )

    group_id = create_response.get_json()["id"]

    client.delete(f"/{user_id}/groups/{group_id}")

    response = client.get("/groups/Anytime Fitness")

    data = response.get_json()
    group = get_group_by_id(data["groups"], group_id)

    assert group is None


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