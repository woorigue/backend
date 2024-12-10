from fastapi.testclient import TestClient


def test_user_login(setup_users, test_app: TestClient):

    user1_email = setup_users["user1"]["user"].email
    data = {"email": user1_email, "password": "test"}
    response = test_app.post("/user/email/login", json=data)
    assert response.status_code == 200


def test_update_user_profile(setup_users, test_app: TestClient):

    user1_token = setup_users["user1"]["token"]
    response = test_app.get(
        "/user/me",
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert response.status_code == 400

    profile_data = {
        "nickname": "User1",
        "gender": "M",
        "location": "서울",
        "age": "2000-12-06T00:00:00",
        "foot": "R",
        "level": 4,
        "positions": [1, 2, 3],
        "is_active": True,
    }
    response = test_app.patch(
        "/user/me",
        json=profile_data,
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert response.status_code == 200

    user2_token = setup_users["user2"]["token"]
    profile_data = {
        "nickname": "User2",
        "gender": "F",
        "location": "서울",
        "age": "1992-02-18T15:53:00",
        "foot": "L",
        "level": 3,
        "positions": [5, 7, 10],
        "is_active": True,
    }
    response = test_app.patch(
        "/user/me",
        json=profile_data,
        headers={"Authorization": f"Bearer {user2_token}"},
    )
    assert response.status_code == 200


def test_get_user_profile(setup_users, test_app: TestClient):

    user1_token = setup_users["user1"]["token"]
    response = test_app.get(
        "/user/me",
        headers={"Authorization": f"Bearer {user1_token}"},
    ).json()
    profile = response["profile"][0]
    profile_data = {
        "user_seq": 1,
        "nickname": "User1",
        "gender": "M",
        "location": "서울",
        "age": "2000-12-06T00:00:00",
        "foot": "R",
        "level": 4,
        "positions": [1, 2, 3],
        "img": None,
    }
    assert profile == profile_data


def test_get_other_user_profile(setup_users, test_app: TestClient):

    user1_token = setup_users["user1"]["token"]
    user_seq = float("inf")
    response = test_app.get(
        "/user/" + str(user_seq),
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert response.status_code, 404

    response = test_app.get(
        "/user/" + str(2),
        headers={"Authorization": f"Bearer {user1_token}"},
    ).json()
    user2_profile = response["profile"][0]
    profile_data = {
        "user_seq": 2,
        "nickname": "User2",
        "gender": "F",
        "location": "서울",
        "age": "1992-02-18T15:53:00",
        "foot": "L",
        "level": 3,
        "positions": [5, 7, 10],
        "img": None,
    }
    assert user2_profile == profile_data
