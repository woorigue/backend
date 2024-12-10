from datetime import datetime
from fastapi.testclient import TestClient
from io import BytesIO


def test_create_club(setup_users, test_app: TestClient):

    user1_token = setup_users["user1"]["token"]

    emblem_img = BytesIO(b"test emblem image data")
    img = BytesIO(b"test image data")

    club_data = {
        "name": "Club1",
        "register_date": "2024-12-06",
        "intro": "안녕하세요, 서울 친목 축구팀입니다.",
        "location": "서울",
        "age_group": "모든연령",
        "membership_fee": "10000",
        "level": "4",
        "gender": "M",
        "uniform_color": "yellow",
    }
    club_files = {
        "emblem_img": ("emblem.jpg", emblem_img, "image/jpeg"),
        "img": ("image.jpg", img, "image/jpeg"),
    }

    response = test_app.post(
        "/club",
        data=club_data,
        files=club_files,
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert response.status_code == 200


def test_get_club(setup_users, test_app: TestClient):

    user1_token = setup_users["user1"]["token"]
    clubs = test_app.get(
        "/club",
        headers={"Authorization": f"Bearer {user1_token}"},
    ).json()

    clubs_data = [
        {
            "seq": 1,
            "name": "Club1",
            "register_date": "2024-12-06",
            "intro": "안녕하세요, 서울 친목 축구팀입니다.",
            "location": "서울",
            "age_group": "모든연령",
            "membership_fee": 10000,
            "level": 4,
            "team_size": 1,
            "gender": "M",
            "emblem_img": "d2al7pp3zcl1yf.cloudfront.net/club/emblem.jpg",
            "img": "d2al7pp3zcl1yf.cloudfront.net/club/image.jpg",
            "uniform_color": "yellow",
        }
    ]
    assert clubs == clubs_data


def test_update_club(setup_users, test_app: TestClient):

    user1_token = setup_users["user1"]["token"]
    club_seq = 1
    club_update_data = {
        "name": "Club1",
        "register_date": "2024-12-06",
        "intro": "안녕하세요, 서울 친목 축구팀입니다.",
        "location": "서울",
        "age_group": "20대",
        "membership_fee": 50000,
        "level": 3,
        "gender": "M",
        "uniform_color": "yellow",
    }

    response = test_app.patch(
        "/club/" + str(club_seq),
        data=club_update_data,
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert response.status_code == 200


def test_get_specific_club(setup_users, test_app: TestClient):

    user1_token = setup_users["user1"]["token"]
    club_seq = 1
    club_data = {
        "seq": 1,
        "name": "Club1",
        "register_date": "2024-12-06",
        "intro": "안녕하세요, 서울 친목 축구팀입니다.",
        "location": "서울",
        "age_group": "20대",
        "membership_fee": 50000,
        "level": 3,
        "team_size": 1,
        "gender": "M",
        "emblem_img": "d2al7pp3zcl1yf.cloudfront.net/club/emblem.jpg",
        "img": "d2al7pp3zcl1yf.cloudfront.net/club/image.jpg",
        "uniform_color": "yellow",
        "roles": {"owner": 1},
    }

    club = test_app.get(
        "/club/" + str(club_seq),
        headers={"Authorization": f"Bearer {user1_token}"},
    ).json()
    assert club == club_data
