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



def test_create_new_order(seeded_client):

    order_request = {
        "user_id": 1,
        "dish_id": 1,
        "order_date": "2025-05-01T21:19:21",
        "total_price": 100.0,
        "is_guest": 0,
    }

    response = seeded_client.post("/orders/", json=order_request)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "order_id" in data
    assert "order_date" in data
    assert data["user_id"] == 1
    assert data["dish_id"] == 1
    assert data["total_price"] == 100.0
    assert data["is_guest"] == 0

    # guest order
    order_request_guest = {
        "user_id": None,
        "dish_id": 1,
        "order_date": "2025-05-01T21:19:21",
        "total_price": 100.0,
        "is_guest": 1,
    }

    response_guest = seeded_client.post("/orders/", json=order_request_guest)
    assert response_guest.status_code == 200
    data_guest = response_guest.json()
    assert isinstance(data_guest, dict)

    assert "order_date" in data_guest
    assert data_guest["dish_id"] == 1
    assert data_guest["total_price"] == 100.0
    assert data_guest["is_guest"] == 1




def test_read_all_orders(seeded_client):
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_update_existing_order(seeded_client):
    order_update = {
        "user_id": 1,
        "dish_id": 2,
        "order_date": "2025-05-01T21:19:21",
        "total_price": 200.0,
        "is_guest": 0,
    }

    response = client.put("/orders/1", json=order_update)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["user_id"] == 1
    assert data["dish_id"] == 2
    assert data["total_price"] == 200.0
    assert data["is_guest"] == 0
    assert "order_id" in data
    assert "order_date" in data



def test_delete_existing_order(seeded_client):
    order_request = {
        "user_id": 1,
        "dish_id": 1,
        "order_date": "2025-05-01T21:19:21",
        "total_price": 100.0,
        "is_guest": 0,
    }

    response = seeded_client.post("/orders/", json=order_request)
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)


    # delete order
    response = seeded_client.delete(f"/orders/{data['order_id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "order_id" in data
    assert data["user_id"] == 1
    assert data["dish_id"] == 1
    assert data["total_price"] == 100.0
    assert data["is_guest"] == 0
    assert "order_date" in data


def test_get_orders_by_range(seeded_client):
    response = seeded_client.get('/orders/by-range', params={
        'start_date': '2025-05-01',
        'end_date': '2025-05-01'
    })
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert all(o['order_date'].startswith('2025-05-01') for o in data)


