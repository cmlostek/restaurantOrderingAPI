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

def test_get_order_details(seeded_client):
    response = seeded_client.get("/orders/1/details/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["detail_id"] == 1
    assert response.json()[1]["detail_id"] == 2


def test_get_order_detail_by_id(seeded_client):
    response = seeded_client.get("/orders/1/details/1")
    assert response.status_code == 200
    assert response.json() == {
        "detail_id": 1,
        "order_id": 1,
        "dish_id": 1,
        "payment_id": 1,
        "order_details": "Requested no mushrooms.",
        "order_status": "Completed"
    }


def test_create_order_detail(seeded_client):
    order_detail_request = {
        "detail_id": 999,
        "order_id": 1,
        "dish_id": 1,
        "payment_id": 1,
        "order_details": "Requested more mushrooms.",
        "order_status": "Pending",
    }
    response = seeded_client.post("/orders/1/details/", json=order_detail_request)
    assert response.status_code == 200
    assert response.json() == {
        "detail_id": 999,
        "order_id": 1,
        "dish_id": 1,
        "payment_id": 1,
        "order_details": "Requested more mushrooms.",
        "order_status": "Pending",
    }


def test_update_order_detail(seeded_client):
    order_detail_update = {
        "detail_id": 1,
        "order_id": 1,
        "dish_id": 1,
        "payment_id": 1,
        "order_details": "Updated order details.",
        "order_status": "In Progress",
    }
    response = seeded_client.put("/orders/1/details/1", json=order_detail_update)
    assert response.status_code == 200
    assert response.json() == {
        "detail_id": 1,
        "order_id": 1,
        "dish_id": 1,
        "payment_id": 1,
        "order_details": "Updated order details.",
        "order_status": "In Progress",
    }


def test_delete_order_detail(seeded_client):
    order_detail = {
        "detail_id": 999,
        "order_id": 1,
        "dish_id": 1,
        "payment_id": 1,
        "order_details": "Requested more mushrooms.",
        "order_status": "Pending",
    }
    response = seeded_client.post("/orders/1/details/", json=order_detail)
    assert response.status_code == 200
    assert response.json() == {
        "detail_id": 999,
        "order_id": 1,
        "dish_id": 1,
        "payment_id": 1,
        "order_details": "Requested more mushrooms.",
        "order_status": "Pending",
    }



