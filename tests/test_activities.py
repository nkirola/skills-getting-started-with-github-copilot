def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_new_participant(client):
    email = "testuser@mergington.edu"
    resp = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for Chess Club"

    get = client.get("/activities")
    assert email in get.json()["Chess Club"]["participants"]


def test_signup_duplicate(client):
    email = "duplicate@mergington.edu"
    # first signup should succeed
    r1 = client.post("/activities/Programming%20Class/signup", params={"email": email})
    assert r1.status_code == 200

    # second signup should fail with 400
    r2 = client.post("/activities/Programming%20Class/signup", params={"email": email})
    assert r2.status_code == 400
    assert "already signed up" in r2.json().get("detail", "")


def test_unregister_participant(client):
    # john@mergington.edu is initially a participant of Gym Class
    email = "john@mergington.edu"
    r = client.delete("/activities/Gym%20Class/participants", params={"email": email})
    assert r.status_code == 200
    assert r.json()["message"] == f"Unregistered {email} from Gym Class"

    get = client.get("/activities")
    assert email not in get.json()["Gym Class"]["participants"]
