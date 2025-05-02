from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture(scope='module')
def seeded_client():
    return client


def test_get_all_reviews(seeded_client):
    response = seeded_client.get('/reviews/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(review['review_id'] == 1 for review in data)


def test_get_review_by_id_and_user(seeded_client):
    resp = seeded_client.get("/reviews/1", params={"user_id": 1})
    assert resp.status_code == 200
    data = resp.json()

    assert data == {
        "review_id": 1,
        "user_id": 1,
        "order_id": 1,
        "rating": 5,
        "comment": "The Chicken Alfredo was creamy and delicious!"
    }

    resp2 = seeded_client.get("/reviews/1", params={"user_id": 2})
    assert resp2.status_code == 404
    assert resp2.json()["detail"] == "Review not found"






def test_create_review_entry(seeded_client):
    payload = {
        "review_id": 4,
        "user_id": 1,
        "order_id": 1,
        "rating": 5,
        "comment": "Absolutely delicious!"
    }
    resp = seeded_client.post(
        "/reviews/",
        params={"user_id": 1},
        json=payload
    )

    data = resp.json()
    assert data ==  {
        "review_id": 4,
        "user_id": 1,
        "order_id": 1,
        "rating": 5,
        "comment": "Absolutely delicious!"
    }



def test_update_review(seeded_client):
    payload = {
        "review_id": 1,
        "user_id": 1,
        "order_id": 1,
        "rating": 4,
        "comment": "The Chicken Alfredo was good, but could be creamier."
    }
    resp = seeded_client.put(
        "/reviews/1",
        params={"user_id": 1},
        json=payload
    )

    data = resp.json()
    assert data == {
        "review_id": 1,
        "user_id": 1,
        "order_id": 1,
        "rating": 4,
        "comment": "The Chicken Alfredo was good, but could be creamier."
    }


def test_delete_review(seeded_client):
    payload = {
        "review_id": 4,
        "user_id": 1,
        "order_id": 1,
        "rating": 5,
        "comment": "This review will be deleted."
    }
    create_resp = seeded_client.post(
        "/reviews/",
        params={"user_id": 1},
        json=payload
    )
    assert create_resp.status_code == 200

    del_resp = seeded_client.delete("/reviews/4", params={"user_id": 1})
    assert del_resp.status_code == 200
    data = del_resp.json()
    assert data["detail"] == "Review deleted successfully"
